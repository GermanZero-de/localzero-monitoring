#!/bin/bash

set -euo pipefail

backup_dir="${1:-}"

if [[ -z "$backup_dir" ]]; then
  latest_backup=$( ls -r -d /data/production/*-*-*-*-*-* | head -1 )
  backup_dir=$latest_backup
fi

if [[ ! -d $backup_dir ]]; then
  echo "Please provide an existing backup folder as the first argument."
  exit 1
fi

source /home/monitoring/testing/.env

# stop the testing app
cd ~/testing/
docker-compose down --volumes

# remove the testing database and images
rm "$DB_PATH"/db.sqlite3
rm -r "$IMAGES_PATH"/uploads/*

# copy the database and images from the prod backup to testing
cp "$backup_dir"/backup_db.sqlite3 "$DB_PATH"/db.sqlite3
cp "$backup_dir"/uploads.tar.gz "$IMAGES_PATH"/uploads.tar.gz
tar -x -f "$IMAGES_PATH"/uploads.tar.gz -C $IMAGES_PATH/uploads/
rm "$IMAGES_PATH"/uploads.tar.gz

# apply migrations using a temporary container
docker run --user=1007:1007 --rm -v /home/monitoring/testing/db:/db cpmonitor:testing sh -c "DJANGO_SECRET_KEY=whatever DJANGO_CSRF_TRUSTED_ORIGINS=https://whatever DJANGO_DEBUG=False python manage.py migrate --settings=config.settings.container"

# start the testing app
docker-compose up --detach --no-build

echo "Finished copying production data to testing successfully!"