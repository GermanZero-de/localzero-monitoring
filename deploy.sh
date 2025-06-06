#!/bin/bash

set -euo pipefail

if [[ "${1:-}" != "testing" && "${1:-}" != "production" ]]; then
    echo "Please provide an environment as the first argument - either \"testing\" or \"production\"!"
    echo "You may additionally pass in a tag suffix as second parameter that will be appended to today's date in the git and docker tags."
    echo
    echo "For example,"
    echo "$ ./deploy.sh testing bugfix"
    echo "will create tags like \"deploy-testing-2023-Aug-05-bugfix\"."
    exit 1
fi

env="${1:-}"
tag_suffix="${2:-}"
if [[ -n "$tag_suffix" ]]; then
    # add leading dash
    tag_suffix=${tag_suffix/#/-}
fi

# Tag the currently checked-out revision with in GitHub
date=$(date +%Y-%m-%d-%H-%M-%S)
tag="deploy-${env}-${date}${tag_suffix}"
echo "Tagging version as $tag in git."
git tag -a $tag -m "Deployment to ${env}"
echo "Pushing tag $tag to github."
git push origin $tag

# Build the image for the Django app
docker compose --env-file .env.${env} build

# Export the images
docker save cpmonitor:${env} -o cpmonitor.tar
docker save klimaschutzmonitor-dbeaver:${env} -o klimaschutzmonitor-dbeaver.tar
docker save nextjs:${env} -o nextjs.tar

# Copy the images, the compose files, the certificate renewal cron job and the reverse proxy settings to the server
scp -C -r nextjs.tar cpmonitor.tar klimaschutzmonitor-dbeaver.tar docker-compose.yml crontab reload-cert.sh backup.sh start-testing-with-prod-data.sh docker/reverseproxy/ monitoring.localzero.net:/tmp/

# Login to the server and execute everything that follows there
ssh -tt monitoring.localzero.net /bin/bash << EOF
set -euo pipefail

# make scripts available
cp /tmp/backup.sh /tmp/start-testing-with-prod-data.sh /home/monitoring/
chmod +x /home/monitoring/backup.sh /home/monitoring/start-testing-with-prod-data.sh

# Import the images into Docker on the server
docker load -i /tmp/cpmonitor.tar
docker load -i /tmp/klimaschutzmonitor-dbeaver.tar
docker load -i /tmp/nextjs.tar

# Tag the images with the current date in case we want to roll back,
# as well as with the environment you're deploying to (to prevent affecting the other environment)
docker tag cpmonitor:${env} cpmonitor:${env}-${date}${tag_suffix}
docker tag klimaschutzmonitor-dbeaver:${env} klimaschutzmonitor-dbeaver:${env}-${date}${tag_suffix}
docker tag nextjs:${env} nextjs:${env}-${date}${tag_suffix}

# backup the db and images
~/backup.sh $env || echo "Backup not possible. Continuing."

# Stop the server, apply the migrations, start the server
cd ~/${env}/
docker-compose down --volumes

# apply migrations using a temporary container
docker run --user=1007:1007 --rm -v /home/monitoring/${env}/db:/db cpmonitor:${env} sh -c "DJANGO_SECRET_KEY=whatever DJANGO_CSRF_TRUSTED_ORIGINS=https://whatever DJANGO_DEBUG=False python manage.py migrate --settings=config.settings.container"

# use the latest docker-compose.yml to start the app using the new image
mv docker-compose.yml docker-compose.yml.bak && cp /tmp/docker-compose.yml .
docker network create testing_nginx_network || echo "Failed to create network testing_nginx_network, but continuing."
docker network create production_nginx_network || echo "Failed to create network production_nginx_network, but continuing."
docker-compose up --detach --no-build

# Update the reverse proxy config
cd ~/reverseproxy
docker-compose down
mv docker-compose.yml docker-compose.yml.bak
cp -r /tmp/reverseproxy/* .
docker-compose up --detach --no-build

# Install certificate renewal cron job
crontab /tmp/crontab
cp /tmp/reload-cert.sh /home/monitoring/
chmod +x /home/monitoring/reload-cert.sh

echo 'FINISHED SUCCESSFULLY!'

exit

EOF
