#!/bin/bash

set -euo pipefail

backup_folder=$1

if [[ -z "$backup_folder" ]]; then
  latest_backup=$( ls -r -d *-*-*-*-*-* | head -1 )
  backup_folder=$latest_backup
fi

if [[ ! -d $backup_folder ]]; then
  echo "Please provide an existing backup folder as the first argument."
  exit 1
fi

env=testing
source /home/monitoring/${env}/.env

# stop the testing app
cd ~/${env}/
docker-compose down --volumes

# remove the testing database and images
rm "$DB_PATH"/db.sqlite3
rm -r "$IMAGES_PATH"/*

# copy the database and images from the prod backup to testing
cp /data/${env}/"$backup_folder"/backup_db.sqlite3 "$DB_PATH"/db.sqlite3
cp /data/${env}/"$backup_folder"/uploads.tar.gz "$IMAGES_PATH"/uploads.tar.gz
tar -x -f "$DB_PATH"/uploads.tar.gz
rm "$DB_PATH"/uploads.tar.gz

# apply migrations using a temporary container
docker run --user=1007:1007 --rm -v /home/monitoring/${env}/db:/db cpmonitor:${env} sh -c "DJANGO_SECRET_KEY=whatever DJANGO_CSRF_TRUSTED_ORIGINS=https://whatever DJANGO_DEBUG=False python manage.py migrate --settings=config.settings.container"

# start the testing app
docker-compose up --detach --no-build