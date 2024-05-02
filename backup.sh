#!/bin/bash

set -euo pipefail

# determine which environment to backup
if [[ "${1:-}" != "testing" && "${1:-}" != "production" ]]; then
    echo "Please provide an environment as the first argument - either \"testing\" or \"production\"!"
    exit 1
fi

env="${1:-}"
source /home/monitoring/${env}/.env

# define place and number of backups
mediaDirectoryInContainer="/images/uploads"
directoryOfBackupInContainer="/backup"
directoryOfBackup=$BACKUP_PATH
maxNumberOfBackups=7

date=$(date +%Y-%m-%d-%H-%M-%S)

# create a new backup
mkdir "$directoryOfBackup"/"$date"
docker exec djangoapp-${env} sqlite3 /db/db.sqlite3 ".backup '$directoryOfBackupInContainer/$date/backup_db.sqlite3'"
docker exec djangoapp-${env} /bin/sh -c "tar -C $mediaDirectoryInContainer -cz -f $directoryOfBackupInContainer/$date/uploads.tar.gz ."

printf "Created a new backup in %s \n" "$directoryOfBackup"/"$date"

# Save logs
if [[ "${env}" = "production" ]]; then
    directoryOfLogs="$directoryOfBackup"/production-logs/"$date"
    mkdir -p ${directoryOfLogs}
    docker logs nginx-${env} > "${directoryOfLogs}"/nginx.log
    printf "Copied logs to %s \n" "${directoryOfLogs}"
fi

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
