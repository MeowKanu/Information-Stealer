"""
generate_fake_browser_data.py

Creates a safe, fake "Local State" JSON and a SQLite "Login Data" DB with
dummy credentials encrypted using AES-GCM with a known key.

Purpose: educational only. Do NOT try this against real browser files.
"""

import os
import json
import base64
import sqlite3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

OUT_DIR = "fake_profile"
LOCAL_STATE = os.path.join(OUT_DIR, "Local State")
LOGIN_DB = os.path.join(OUT_DIR, "Login Data")


def ensure_out():
    os.makedirs(OUT_DIR, exist_ok=True)


def generate_key():
    # AES-256 key (32 bytes)
    key = AESGCM.generate_key(bit_length=256)
    return key


def write_local_state(key_bytes):
    # In real Chrome the key may be wrapped; here we store a base64 key
    local_state = {
        "os_crypt": {
            "encrypted_key": base64.b64encode(key_bytes).decode()
        },
        "simulated": True
    }
    with open(LOCAL_STATE, "w", encoding="utf-8") as f:
        json.dump(local_state, f, indent=2)
    print(f"[+] Wrote fake Local State -> {LOCAL_STATE}")


def create_login_db(key_bytes, entries):
    # Create sqlite DB and a logins table with encrypted password blob
    if os.path.exists(LOGIN_DB):
        os.remove(LOGIN_DB)

    conn = sqlite3.connect(LOGIN_DB)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin_url TEXT,
            username_value TEXT,
            password_value BLOB
        );
        """
    )

    aesgcm = AESGCM(key_bytes)

    for origin, user, plain_pwd in entries:
        nonce = os.urandom(12)  # AES-GCM nonce
        ct = aesgcm.encrypt(nonce, plain_pwd.encode("utf-8"), None)
        # store nonce + ciphertext as base64 so it's easy to move between systems
        blob = base64.b64encode(nonce + ct)
        c.execute("INSERT INTO logins (origin_url, username_value, password_value) VALUES (?, ?, ?)",
                  (origin, user, blob))
        print(f"[+] Added entry for {origin} / {user}")

    conn.commit()
    conn.close()
    print(f"[+] Wrote fake Login Data -> {LOGIN_DB}")


def main():
    ensure_out()
    key = generate_key()
    write_local_state(key)
    # sample dummy credentials
    entries = [
        ("https://example.com", "alice", "alice_pass_123"),
        ("https://institute.edu", "bob", "bob_secret"),
        ("https://bank.test", "carol", "carol_pw!@#"),
    ]
    create_login_db(key, entries)
    print("\n[!] Fake profile created in folder:", OUT_DIR)
    print("[!] This is SAFE test data — do not confuse with real browser files.")


if __name__ == "__main__":
    main()
