import subprocess
import pyautogui
import time
import os

# Path to Notepad++ executable (change if your installation is different)
notepad_plus_path = r"C:\Program Files\Notepad++\notepad++.exe"

# Open Notepad++
subprocess.Popen([notepad_plus_path])

# Wait for Notepad++ to open
time.sleep(2)  # Adjust if your PC is slow

# Type "Hello World"
pyautogui.typewrite("Hello World", interval=0.05)
