import urequests # type: ignore
import machine # type: ignore
import json

BASE_RAW_URL = "https://raw.githubusercontent.com/ian-antking/tram-unicorn/main/"

VERSION_URL = BASE_RAW_URL + "version.txt"
FILES_LIST_URL = BASE_RAW_URL + "update-files.json"

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

def get_local_version():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except Exception as e:
        print("Failed to read local version:", e)
        return None

def get_files_to_update():
    try:
        r = urequests.get(FILES_LIST_URL)
        if r.status_code == 200:
            files = json.loads(r.text)
            r.close()
            return files
        r.close()
    except Exception as e:
        print("Failed to fetch files list:", e)
    return []

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

def perform_update(screen):
    screen.display_message(["checking for updates..."])
    local_version = get_local_version()
    remote_version = get_remote_version()
    if remote_version is None:
        print("Could not retrieve remote version. Skipping update.")
        return

    print(f"Local version: {local_version}")
    print(f"Remote version: {remote_version}")

    screen.display_message(["downloading version", remote_version])

    if remote_version != local_version:
        print("New version detected, updating files...")
        files_to_update = get_files_to_update()
        for f in files_to_update:
            success = download_file(f)
            if not success:
                print("Update failed.")
                return
        print("Update successful, rebooting...")
        screen.display_message(["update successful", "rebooting"])
        machine.reset()
    else:
        screen.display_message(["device is up to date"])
        print("Device is up to date.")
