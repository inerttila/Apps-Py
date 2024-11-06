import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_commands_as_admin():
    commands = [
        'wsl --shutdown',
        'wsl --unregister Ubuntu-24.04',
        'wsl --unregister docker-desktop',
        'wsl --install -d Ubuntu-24.04'
    ]

    # Run the first three commands without showing the command prompt
    for command in commands[:-1]:
        print(f"Executing (silent): {command}")
        subprocess.run(command, shell=True)

    # For the last command, show the command line
    last_command = commands[-1]
    print(f"Executing: {last_command}")
    subprocess.Popen(['cmd.exe', '/k', last_command])

if __name__ == "__main__":
    # Check if the script is running as admin
    if not is_admin():
        # Re-run the program with admin privileges
        print("Requesting administrator access...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        run_commands_as_admin()
