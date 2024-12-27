# Crop-Merge
This app is used for cropping orthophotos, preparing them for training to generate a pre-trained model.

The reason for adding the environment is because changes were made to the file 
```bash
"Crop-Merge\env\Lib\site-packages\PIL\Image.py".
```

From this:
```bash
MAX_IMAGE_PIXELS: int | None = int(1024 * 1024 * 1024 // 4 // 3)
```

To this:
```bash
MAX_IMAGE_PIXELS: int | None = None
```

You can either install your own environment or use this one.

Make sure to have the following Python version. You can check it in the file 
```bash
"Crop-Merge\env\pyvenv.cfg"
 ```

# FOCALBOARD-BACKUP
## This readme is for the [focalboard](https://github.com/mattermost-community/focalboard) project

To create a backup, run the `backup.pyw` file
To restore a backup, run the `restore.pyw` file

## New Edition

With this new version, there’s no need to run these commands manually! Now, simply start the app with the following command, and the app will automatically locate the "data" directory and manage the backup.
Ensure you start the app with this command before using it or adding data.

The "data" directory will be saved at: `/mnt/d/focalboard_TOOLS/data ` which is mapped from: `/opt/focalboard/data `

## Starting the App in WSL and including the restart comand after the Docker is shutdown/start

```
docker run -it --name focalboard --restart unless-stopped -p 9001:8000 -v /mnt/d/focalboard_TOOLS/data:/opt/focalboard/data mattermost/focalboard
```

# GET-DATA
## These apps are used to scrape data from 3dskai and skaitech webpages, including product names and their prices.


# KILL-WSL
## This app is used to delete the WSL disk and to delete temporary files.


# UBUNTU-INSTALL
This app uninstalls and reinstalls the Ubuntu WSL distribution.

### Usage

Run the script with administrator privileges to execute the following commands:
- Shutdown WSL
- Unregister Ubuntu-24.04
- Unregister Docker Desktop
- Reinstall Ubuntu-24.04