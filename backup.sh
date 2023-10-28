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
maxNumberOfBackups=3

date=$(date +%Y-%m-%d-%H-%M-%S)

# create a new backup
mkdir -m a+rw "$directoryOfBackup"/"$date"
docker exec djangoapp-testing sqlite3 /db/db.sqlite3 ".backup '$directoryOfBackupInContainer/$date/backup_db.sqlite3'"
docker exec djangoapp-testing /bin/sh -c "python manage.py mediabackup --settings=config.settings.container -O $directoryOfBackupInContainer/$date/media.tar"
docker exec djangoapp-testing chmod a+rw "$directoryOfBackupInContainer"/"$date"/backup_db.sqlite3
docker exec djangoapp-testing chmod a+rw "$directoryOfBackupInContainer"/"$date"/media.tar

printf "Created a new backup in %s \n" "$directoryOfBackup"/"$date"

# delete the oldest backups
cd "$directoryOfBackup"

existingBackupFolders=$( ls -d *-*-*-*-*-* )
numberOfBackups=$( echo "$existingBackupFolders" | wc -l )

while [ $numberOfBackups -gt $maxNumberOfBackups ]
do
  oldestBackupFolder=$( echo "$existingBackupFolders" | head -1 )
  rm -r "$oldestBackupFolder"
  printf "Deleted old backup: %s \n" "$directoryOfBackup/$oldestBackupFolder"

  existingBackupFolders=$( ls -d *-*-*-*-*-* )
  numberOfBackups=$( echo "$existingBackupFolders" | wc -l )
done
