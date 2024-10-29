import os
import subprocess

def restore_focalboard_data(container_name, backup_dir):
    # Define the target directory in the container
    target_dir = "/opt/focalboard/data"

    # Check if the backup directory exists
    if not os.path.exists(backup_dir):
        print(f"Backup directory '{backup_dir}' does not exist.")
        return

    # Ensure the container is running
    container_status = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
        capture_output=True,
        text=True
    )

    if container_status.returncode != 0 or "false" in container_status.stdout:
        print(f"Container {container_name} is not running. Please start the container.")
        return

    # Copy the backup data into the container
    print(f"Restoring data from {backup_dir} to {container_name}:{target_dir}")
    result = subprocess.run(
        ["docker", "cp", backup_dir, f"{container_name}:{target_dir}"],
        capture_output=True,
        text=True
    )

    # Check for errors
    if result.returncode != 0:
        print("Error during restoration:", result.stderr)
    else:
        print("Data restoration completed successfully.")

if __name__ == "__main__":
    container_name = "focalboard"  # Container name
    backup_directory = "/mnt/d/focalboard_TOOLS"  # Update to the correct backup path

    restore_focalboard_data(container_name, backup_directory)
