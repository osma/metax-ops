#!/bin/sh

nextcloudcmd -u {{ metax_backup_username }} -p '{{ metax_backup_password }}' {{ metax_db_backup_archive_path }} https://kannu.csc.fi/remote.php/webdav/METAX_DB_BACKUP
