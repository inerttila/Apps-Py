import subprocess
import os
import shutil
import ctypes
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True)
        print(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")

def delete_files_in_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
    except PermissionError:
        print(f"Permission denied for folder '{folder_path}'.")

def is_admin():
    """ Check if the script is being run with admin privileges. """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """ Rerun the script with admin privileges. """
    if sys.platform == "win32":
        # Create a new process with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    else:
        print("This script can only be run on Windows.")
    sys.exit()

def main():
    if not is_admin():
        print("This script needs to be run as Administrator.")
        run_as_admin()

    # Shutdown WSL
    run_command("wsl --shutdown")

    # Delete contents of C:\Users\User\AppData\Local\Docker\wsl\disk
    docker_wsl_disk_path = r"C:\Users\User\AppData\Local\Docker\wsl\disk"
    delete_files_in_folder(docker_wsl_disk_path)

    # Delete contents of C:\Users\User\AppData\Local\Temp
    temp_folder_path = r"C:\Users\User\AppData\Local\Temp"
    delete_files_in_folder(temp_folder_path)

    # Delete contents of C:\Windows\Temp
    windows_temp_folder_path = r"C:\Windows\Temp"
    delete_files_in_folder(windows_temp_folder_path)

    # Delete contents of C:\Windows\Prefetch
    windows_prefetch_folder_path = r"C:\Windows\Prefetch"
    delete_files_in_folder(windows_prefetch_folder_path)

if __name__ == "__main__":
    main()
