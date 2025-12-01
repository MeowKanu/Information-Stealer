"""
detector.py

Safe auditor: checks default Chrome/Chromium/Brave paths for Local State and Login Data
and optionally copies them into an analysis folder for offline study.

This does NOT decrypt anything.
"""

import os
import platform
import shutil

DEST = "artifact_copies"


def chrome_candidates():
    home = os.path.expanduser("~")
    system = platform.system()
    candidates = []
    if system == "Windows":
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        base = os.path.join(local_appdata, "Google", "Chrome", "User Data", "Default")
        candidates = [
            os.path.join(base, "Local State"),
            os.path.join(base, "Login Data"),
        ]
    else:
        candidates = [
            os.path.join(home, ".config", "google-chrome", "Default", "Local State"),
            os.path.join(home, ".config", "google-chrome", "Default", "Login Data"),
            os.path.join(home, ".config", "chromium", "Default", "Local State"),
            os.path.join(home, ".config", "chromium", "Default", "Login Data"),
            os.path.join(home, "Library", "Application Support", "Google", "Chrome", "Default", "Local State"),  # mac
            os.path.join(home, "Library", "Application Support", "Google", "Chrome", "Default", "Login Data"),
        ]
    return candidates


def find_and_copy():
    os.makedirs(DEST, exist_ok=True)
    candidates = chrome_candidates()
    found = []
    for p in candidates:
        if os.path.exists(p):
            dst = os.path.join(DEST, os.path.basename(p))
            try:
                shutil.copy2(p, dst)
                found.append(dst)
            except Exception as e:
                print(f"Failed to copy {p}: {e}")
    return found


def main():
    print("[*] Searching for common browser artifacts (safe, read-only detection)...")
    found = find_and_copy()
    if not found:
        print("No standard artifacts found in default locations.")
    else:
        print("Copied the following artifacts to:", DEST)
        for f in found:
            print(" -", f)
    print("\nNote: This script does NOT decrypt anything. Use analysis VMs for deeper study.")


if __name__ == "__main__":
    main()
python detector.py
