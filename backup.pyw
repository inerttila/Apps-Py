import os
import subprocess
import shutil

def backup_focalboard_data(container_name, backup_dir):
    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Define the source directory in the container
    source_dir = "/opt/focalboard/data"

    # Remove existing backup if it exists
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)

    # Check if the container is running
    container_status = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", container_name], 
        capture_output=True, 
        text=True
    )

    if container_status.returncode != 0 or "false" in container_status.stdout:
        print(f"Container {container_name} is not running.")
        return

    # Use Docker cp to copy files from the container to the local backup directory
    print(f"Backing up data from {container_name}:{source_dir} to {backup_dir}")
    result = subprocess.run(
        ["docker", "cp", f"{container_name}:{source_dir}", backup_dir], 
        capture_output=True, 
        text=True
    )

    # Check for errors
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print("Backup completed successfully.")

if __name__ == "__main__":
    container_name = "focalboard"  # Container name
    backup_directory = "/mnt/d/focalboard_TOOLS"  # Local directory for backup

    backup_focalboard_data(container_name, backup_directory)


