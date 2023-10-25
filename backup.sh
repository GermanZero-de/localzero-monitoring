#!/bin/bash

set -euo pipefail

# determine which environment to backup
if [[ "${1:-}" != "testing" && "${1:-}" != "production" ]]; then
    echo "Please provide an environment as the first argument - either \"testing\" or \"production\"!"
    exit 1
fi

env="${1:-}"
source .env.${env}

# define place and number of backups
directoryOfBackupInContainer="/backup"
directoryOfBackup=$BACKUP_PATH
maxNumberOfBackups=7

date=$(date +%Y-%m-%d-%H-%M-%S)

# create a new backup
docker exec djangoapp-testing cd /backup
docker exec djangoapp-testing mkdir /$date
docker exec djangoapp-testing sqlite3 db.sqlite3 ".backup 'backup_file.sq3'"
docker exec djangoapp-testing /bin/sh -c "python -Xutf8 manage.py dumpdata -e contenttypes -e auth.Permission -e admin.LogEntry -e sessions --indent 2 --settings=config.settings.container > $directoryOfBackupInContainer/$date/database.json"
docker exec djangoapp-testing /bin/sh -c "python manage.py mediabackup --settings=config.settings.container -O $directoryOfBackupInContainer/$date/media.tar"

printf "Created a new backup in %s \n" $directoryOfBackup/$date

# delete the oldest backups
cd $directoryOfBackup || { echo "Could not enter directory $directoryOfBackup"; exit 126; }

existingBackupFolders=$( ls -d *-*-*-*-*-* )
numberOfBackups=$( echo "$existingBackupFolders" | wc -l )

while [ $numberOfBackups -gt $maxNumberOfBackups ]
do
  oldestBackupFolder=$( echo "$existingBackupFolders" | head -1 )
  rm -r $oldestBackupFolder
  printf "Deleted old backup: %s \n" "$directoryOfBackup/$oldestBackupFolder"

  existingBackupFolders=$( ls -d *-*-*-*-*-* )
  numberOfBackups=$( echo "$existingBackupFolders" | wc -l )
done
