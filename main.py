import os
import sys
import time
import logging
import subprocess
import shutil
import platform
import getpass

# ---------- Audit log ----------
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

logging.info("Script started. User=%s Machine=%s Python=%s CWD=%s",
             getpass.getuser(), platform.node(), sys.version, os.getcwd())

# ---------- Headless detection ----------
def is_headless():
    try:
        import ctypes
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0) == 0 or user32.GetSystemMetrics(1) == 0
    except Exception:
        return True

HEADLESS = os.environ.get("FORCE_HEADLESS") == "1" or is_headless()

if HEADLESS:
    logging.warning("No interactive desktop detected. Using headless fallback.")
    out = os.path.abspath("hello_world.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("Hello World")
    logging.info("Wrote %s", out)
    logging.info("Finished (headless). Log: %s", LOG_FILE)
    sys.exit(0)

# ---------- Import pyautogui (must be installed via requirements.txt) ----------
try:
    import pyautogui
except ImportError:
    logging.error("pyautogui is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# ---------- Find Notepad++ or fallback ----------
def find_npp():
    candidates = [
        r"C:\Program Files\Notepad++\notepad++.exe",
        r"C:\Program Files (x86)\Notepad++\notepad++.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Notepad++\notepad++.exe"),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return shutil.which("notepad++") or shutil.which("notepad++.exe")

editor = find_npp()
if editor and os.path.exists(editor):
    logging.info("Launching Notepad++: %s", editor)
    subprocess.Popen([editor])
else:
    logging.warning("Notepad++ not found. Launching Notepad.")
    subprocess.Popen(["notepad.exe"])

time.sleep(3)

try:
    logging.info("Typing 'Hello World'...")
    pyautogui.write("Hello World", interval=0.05)
    logging.info("Done typing.")
except Exception as e:
    logging.exception("Typing failed: %s", e)
    sys.exit(1)

logging.info("Finished. Log: %s", LOG_FILE)
