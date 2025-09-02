import subprocess
import sys
import time

def install_dependencies():
    """Install required dependencies if missing."""
    try:
        import pyautogui  # noqa
    except ImportError:
        print("pyautogui not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
        print("pyautogui installed successfully.")

def run():
    """Do the primary process of the robot."""
    import pyautogui

    print("HEY!!!!!")
    subprocess.Popen(["notepad.exe"])
    time.sleep(3)
    pyautogui.write("Hello World", interval=0.2)


if __name__ == "__main__":
    install_dependencies()
    run()

