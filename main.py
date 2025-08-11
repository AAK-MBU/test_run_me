import subprocess
import sys
import time
import os

# Ensure pyautogui is installed
try:
    import pyautogui
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

# Path to Notepad++ executable (change if needed)
notepad_plus_path = r"C:\Program Files\Notepad++\notepad++.exe"

if not os.path.exists(notepad_plus_path):
    raise FileNotFoundError(f"Notepad++ not found at: {notepad_plus_path}")

# Open Notepad++
subprocess.Popen([notepad_plus_path])

# Wait for Notepad++ to open
time.sleep(2)  # Increase if needed

# Type "Hello World"
pyautogui.typewrite("Hello World", interval=0.05)
