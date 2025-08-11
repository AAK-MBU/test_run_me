import os
import sys
import time
import logging
import subprocess
import shutil
import platform
import getpass

# -----------------------
# Audit logging setup
# -----------------------
LOG_FILE = os.path.abspath("script_audit.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logging.getLogger().addHandler(console)

logging.info("Script started.")
logging.info("User: %s | Machine: %s | Python: %s", getpass.getuser(), platform.node(), sys.version)
logging.info("Working dir: %s", os.getcwd())

# -----------------------
# Helper: install a package via pip
# -----------------------
def ensure_package(pkg: str):
    try:
        __import__(pkg)
        logging.info("Package '%s' already installed.", pkg)
    except ImportError:
        logging.warning("Package '%s' not found; installing...", pkg)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            __import__(pkg)
            logging.info("Package '%s' installed successfully.", pkg)
        except Exception as e:
            logging.exception("Failed to install '%s': %s", pkg, e)
            sys.exit(1)

# Ensure pyautogui (and its dependencies) is available
ensure_package("pyautogui")

# Now we can import it
import pyautogui

# Optional: make typing a bit safer
pyautogui.FAILSAFE = True  # move mouse to a corner to abort
pyautogui.PAUSE = 0.05

# -----------------------
# Locate Notepad++ (or fall back to Notepad)
# -----------------------
def find_notepad_plus_plus():
    # 1) Check common install locations
    candidates = [
        r"C:\Program Files\Notepad++\notepad++.exe",
        r"C:\Program Files (x86)\Notepad++\notepad++.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Notepad++\notepad++.exe"),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p

    # 2) Try Windows registry
    try:
        import winreg
        keys = [
            r"SOFTWARE\Notepad++",  # 64-bit hive
            r"SOFTWARE\WOW6432Node\Notepad++",  # 32-bit on 64-bit
        ]
        for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for k in keys:
                try:
                    with winreg.OpenKey(root, k) as key:
                        install_dir, _ = winreg.QueryValueEx(key, "DisplayIcon")
                        if install_dir and os.path.exists(install_dir):
                            return install_dir
                except OSError:
                    continue
    except Exception:
        # winreg might not be available or accessible
        pass

    # 3) Try PATH
    exe = shutil.which("notepad++") or shutil.which("notepad++.exe")
    if exe:
        return exe

    return None

def launch_editor():
    npp = find_notepad_plus_plus()
    if npp and os.path.exists(npp):
        logging.info("Launching Notepad++ at: %s", npp)
        try:
            subprocess.Popen([npp])
            return "notepad++"
        except Exception as e:
            logging.exception("Failed to launch Notepad++: %s", e)

    logging.warning("Notepad++ not found. Falling back to Windows Notepad.")
    # Launch plain Notepad as a fallback so the script still works
    try:
        subprocess.Popen(["notepad.exe"])
        return "notepad"
    except Exception as e:
        logging.exception("Failed to launch Notepad as well: %s", e)
        sys.exit(1)

editor = launch_editor()

# -----------------------
# Give the window time / focus and type
# -----------------------
# If your machine is slower or if plugins load in Notepad++, increase this.
delay_seconds = 3 if editor == "notepad++" else 2
logging.info("Waiting %s seconds for the editor to be ready...", delay_seconds)
time.sleep(delay_seconds)

try:
    logging.info("Typing 'Hello World'...")
    pyautogui.write("Hello World", interval=0.05)
    logging.info("Typing complete.")
except Exception as e:
    logging.exception("Typing failed: %s", e)
    sys.exit(1)

logging.info("Script finished successfully. Log written to: %s", LOG_FILE)
