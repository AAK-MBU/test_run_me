import os
import shutil
import subprocess
import sys
import tempfile
import time

import pyautogui  # already installed via requirements.txt

def find_notepad_plus():
    hit = shutil.which("notepad++.exe")
    if hit:
        return hit

    candidates = [
        r"C:\Program Files\Notepad++\notepad++.exe",
        r"C:\Program Files (x86)\Notepad++\notepad++.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c

    npp_env = os.environ.get("NPP_PATH")
    if npp_env and os.path.exists(npp_env):
        return npp_env
    return None

def run():
    print("Im running...")
    npp = find_notepad_plus()
    if not npp:
        tmp = os.path.join(tempfile.gettempdir(), "hello_from_worker.txt")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("Hello World")
        print(f"Notepad++ not found. Wrote {tmp} instead.")
        sys.exit(0)

    subprocess.Popen([npp])
    time.sleep(3)
    pyautogui.write("Hello World", interval=0.2)
    print("I ended =)")

if __name__ == "__main__":
    run()
