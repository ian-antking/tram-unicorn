import zipfile
import os
import sys

EXCLUDE_FILES = {
    "CONFIG.py",
    "WIFI_CONFIG.py",
    "CONFIG.example.py",
    "WIFI_CONFIG.example.py",
    ".gitignore",
    "build_release.py",
    ".DS_Store",
}

def should_exclude(file):
    return (
        file in EXCLUDE_FILES
        or file.startswith(".")
        or file.endswith("~")
        or file.endswith(".pyc")
        or "__pycache__" in file
    )

def build_release(version):
    zip_filename = f"firmware-{version}.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("."):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), ".")
                if should_exclude(rel_path):
                    continue
                zipf.write(rel_path)
                print(f"✅ Added: {rel_path}")

    print(f"\n🎉 Release built: {zip_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_release.py <version>")
        sys.exit(1)

    version = sys.argv[1].strip()
    build_release(version)
