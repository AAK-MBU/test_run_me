import subprocess
import sys
import time
import shutil
import importlib.util

DEPENDENCIES = ["pyautogui"]


def _check_uv_available():
    if shutil.which("uv") is None:
        raise RuntimeError(
            "The 'uv' CLI is not available on PATH. "
            "Install it and try again."
        )


def _missing_packages(names):
    missing = []
    for name in names:
        if importlib.util.find_spec(name) is None:
            missing.append(name)
    return missing


def ensure_dependencies_with_uv(packages):
    """Install missing packages using uv-only (and pip via `uv pip`)."""
    _check_uv_available()

    to_install = _missing_packages(packages)
    if not to_install:
        return

    python = sys.executable

    subprocess.run(
        ["uv", "pip", "install", "--python", python, "--upgrade", "pip"],
        check=True,
    )

    subprocess.run(
        ["uv", "pip", "install", "--python", python, *to_install],
        check=True,
    )


def run():
    ensure_dependencies_with_uv(DEPENDENCIES)

    import pyautogui

    print("HEY!!!!!")
    subprocess.Popen(["notepad.exe"])
    time.sleep(3)
    pyautogui.write("Hello World", interval=0.2)


if __name__ == "__main__":
    run()
