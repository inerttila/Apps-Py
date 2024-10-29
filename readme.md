to create the backup run the

```
backup.pyw
```

to run the app although you have no data to be save on wsl run

```
docker run -it --name focalboard -p 9001:8000 -v /mnt/d/focalboard_TOOLS/data:/opt/focalboard/data mattermost/focalboard
```
