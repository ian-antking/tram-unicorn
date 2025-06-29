import urequests # type: ignore
import machine # type: ignore
from version import CURRENT_VERSION

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/ian-antking/tram-unicorn/main/"

VERSION_URL = GITHUB_RAW_BASE + "version.txt"
BASE_RAW_URL = GITHUB_RAW_BASE


FILES_TO_UPDATE = [
    "main.py",
    "app.py",
    "API.py",
    "network_manager.py",
    "repository.py",
    "screen_controller.py",
    "scroll_text.py",
    "tram.py",
    "COLORS.py",
    "VERSION.py",
]

def get_remote_version():
    try:
        r = urequests.get(VERSION_URL)
        if r.status_code == 200:
            remote_version = r.text.strip()
            r.close()
            return remote_version
        r.close()
    except Exception as e:
        print(e)
        print("Failed to get remote version:", e)
    return None

def download_file(filename):
    try:
        url = BASE_RAW_URL + filename
        print("Downloading", url)
        r = urequests.get(url)
        if r.status_code == 200:
            with open(filename, "w") as f:
                f.write(r.text)
            print(f"Updated {filename}")
            r.close()
            return True
        r.close()
    except Exception as e:
        print(f"Failed to download {filename}:", e)
    return False

def perform_update():
    remote_version = get_remote_version()
    if remote_version is None:
        print("Could not retrieve remote version. Skipping update.")
        return

    print(f"Local version: {CURRENT_VERSION}")
    print(f"Remote version: {remote_version}")

    if remote_version != CURRENT_VERSION:
        print("New version detected, updating files...")
        for f in FILES_TO_UPDATE:
            success = download_file(f)
            if not success:
                print("Update failed.")
                return
        print("Update successful, rebooting...")
        machine.reset()
    else:
        print("Device is up to date.")
