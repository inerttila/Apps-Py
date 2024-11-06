# FOCALBOARD-BACKUP

## This readme is for the [focalboard](https://github.com/mattermost-community/focalboard) project

To create a backup, run the `backup.pyw` file
To restore a backup, run the `restore.pyw` file

## New Edition

With this new version, there’s no need to run these commands manually! Now, simply start the app with the following command, and the app will automatically locate the "data" directory and manage the backup.
Ensure you start the app with this command before using it or adding data.

The "data" directory will be saved at: `/mnt/d/focalboard_TOOLS/data ` which is mapped from: `/opt/focalboard/data `

## Starting the App in WSL

```
docker run -it --name focalboard -p 9001:8000 -v /mnt/d/focalboard_TOOLS/data:/opt/focalboard/data mattermost/focalboard
```
