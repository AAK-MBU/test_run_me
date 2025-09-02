import subprocess
import sys
import time
import shutil

def ensure_pyautogui():
    """Install pyautogui into this interpreter using uv pip if missing."""
    try:
        import pyautogui  # noqa
    except ImportError:
        if shutil.which("uv") is None:
            raise RuntimeError("uv CLI not found on PATH")
        subprocess.run(
            ["uv", "pip", "install", "--python", sys.executable, "pyautogui"],
            check=True,
        )

def run():
    ensure_pyautogui()
    import pyautogui

    print("HEY!!!!!")

    subprocess.Popen(["notepad++.exe"])
    time.sleep(3)

    pyautogui.write("Hello World", interval=0.2)

if __name__ == "__main__":
    run()
