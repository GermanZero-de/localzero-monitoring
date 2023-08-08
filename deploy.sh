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

# 2
date=$(date +%Y-%b-%d)
tag="deploy-${env}-${date}${tag_suffix}"
echo "Tagging version as $tag in git."
git tag -a $tag -m "Deployment to ${env}" && git push origin $tag

#3
docker compose build

# 4
docker save cpmonitor -o cpmonitor.tar
docker save klimaschutzmonitor-dbeaver -o klimaschutzmonitor-dbeaver.tar

# 5
scp -C cpmonitor.tar klimaschutzmonitor-dbeaver.tar docker-compose.yml crontab renew-cert.sh monitoring@monitoring.localzero.net:/tmp/

ssh -tt lzm /bin/bash << EOF
set -euo pipefail

# 7
docker load -i /tmp/cpmonitor.tar
docker load -i /tmp/klimaschutzmonitor-dbeaver.tar

# 8
# TODO something about the tagging doesn't work as it should, do local tags not match what we expect here?
docker tag cpmonitor:${env} cpmonitor:${date}${tag_suffix}
docker tag klimaschutzmonitor-dbeaver:${env} klimaschutzmonitor-dbeaver:${date}${tag_suffix}

# 9
cd ~/${env}/
docker-compose down --volumes
# backup the db
cp -v db/db.sqlite3 /data/LocalZero/DB_BACKUPS/${env}/db.sqlite3.${date}${tag_suffix}
cp -vr cpmonitor/images/uploads /data/LocalZero/DB_BACKUPS/${env}/uploads.${date}${tag_suffix}
# apply migrations using a temporary container
# this doesn't seem to work like it should; migrations were not applied last time
docker run --user=1007:1007 --rm -v /home/monitoring/${env}/db:/db cpmonitor:${env} sh -c "DJANGO_SECRET_KEY=whatever DJANGO_CSRF_TRUSTED_ORIGINS=https://whatever DJANGO_DEBUG=False python manage.py migrate --settings=config.settings.container"

# use the latest docker-compose.yml to start the app using the new image
mv docker-compose.yml docker-compose.yml.bak && cp /tmp/docker-compose.yml .
docker-compose up --detach --no-build

# 10
crontab /tmp/crontab
cp /tmp/renew-cert.sh /home/monitoring/
chmod +x /home/monitoring/renew-cert.sh

echo
echo 'FINISHED SUCCESSFULLY!'
echo

EOF