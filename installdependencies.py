import os
import subprocess
import sys

def install_requirements():
    """Automatically installs the required Python packages."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies have been successfully installed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
