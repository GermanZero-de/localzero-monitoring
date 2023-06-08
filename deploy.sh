#!/bin/bash

set -euo pipefail
set -x

if [[ "${1:-}" != "testing" && "${1:-}" != "production" ]]; then
    echo "Please provide an environment as the first argument - either \"testing\" or \"production\"!"
    exit 1
fi

env="${1:-}"

# 2
DATESTR=$(date +%Y-%b-%d) && echo "Using timestamp ${DATESTR}."
git tag -a deploy-${env}-${DATESTR} -m "Deployment to test" && git push origin deploy-${env}-${DATESTR}

#3
docker compose build

# 4
docker save cpmonitor -o cpmonitor.tar
docker save klimaschutzmonitor-dbeaver -o klimaschutzmonitor-dbeaver.tar

# 5
scp -C cpmonitor.tar klimaschutzmonitor-dbeaver.tar docker-compose.yml crontab renew-cert.sh monitoring@monitoring.localzero.net:/tmp/

# 6
ssh lzm /bin/bash << EOF

# 7
docker load -i /tmp/cpmonitor.tar
docker load -i /tmp/klimaschutzmonitor-dbeaver.tar

# 8
docker tag cpmonitor:latest cpmonitor:${DATESTR}
docker tag klimaschutzmonitor-dbeaver:latest klimaschutzmonitor-dbeaver:${DATESTR}

# 9
cd ~/${env}/
docker-compose down --volumes
# backup the db
cp -v db/db.sqlite3 /data/LocalZero/DB_BACKUPS/${env}/db.sqlite3.${DATESTR}
cp -vr cpmonitor/images/uploads /data/LocalZero/DB_BACKUPS/testing/uploads.${DATESTR}
# apply migrations using a temporary container
docker run --user=1007:1007 --rm -it -v $(pwd)/db:/db cpmonitor:latest sh
DJANGO_SECRET_KEY=whatever DJANGO_CSRF_TRUSTED_ORIGINS=https://whatever DJANGO_DEBUG=False python manage.py migrate --settings=config.settings.container
# exit and stop the temporary container
exit
# use the latest docker-compose.yml to start the app using the new image
mv docker-compose.yml docker-compose.yml.bak && cp /tmp/docker-compose.yml .
docker-compose up --detach --no-build

# 10
crontab /tmp/crontab
cp /tmp/renew-cert.sh /home/monitoring/
chmod +x /home/monitoring/renew-cert.sh

EOF