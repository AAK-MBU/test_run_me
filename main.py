import subprocess
import sys
import time
import os
import logging

# --- Audit Log Setup ---
log_file = "script_audit.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Script started.")

# Ensure pyautogui is installed
try:
    import pyautogui
    logging.info("pyautogui already installed.")
except ImportError:
    logging.warning("pyautogui not found. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
        import pyautogui
        logging.info("pyautogui installed successfully.")
    except Exception as e:
        logging.error(f"Failed to install pyautogui: {e}")
        sys.exit(1)

# Path to Notepad++ executable
notepad_plus_path = r"C:\Program Files\Notepad++\notepad++.exe"

if not os.path.exists(notepad_plus_path):
    logging.error(f"Notepad++ not found at: {notepad_plus_path}")
    raise FileNotFoundError(f"Notepad++ not found at: {notepad_plus_path}")

# Open Notepad++
logging.info("Launching Notepad++...")
subprocess.Popen([notepad_plus_path])

# Wait for Notepad++ to open
time.sleep(2)  # Adjust if needed

# Type "Hello World"
logging.info("Typing 'Hello World' into Notepad++.")
pyautogui.typewrite("Hello World", interval=0.05)

logging.info("Script finished successfully.")
