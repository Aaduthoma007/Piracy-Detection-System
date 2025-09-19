# main.py - Driver script for Content Piracy Detection System
# Run with: python main.py

import os
import subprocess  # To run your other scripts

# Config - adjust these if needed
ORIGINAL_VIDEO = "Original.mp4"
SUSPECT_VIDEO = "suspect.mp4"
JSON_DB = "original_db.json"
SQLITE_DB = "fingerprints.db"

def run_build_fingerprint():
    if not os.path.exists(ORIGINAL_VIDEO):
        print(f"Error: Original video '{ORIGINAL_VIDEO}' not found!")
        return
    print("Building fingerprint from original video...")
    subprocess.run(["python", "build_fingerprint.py", ORIGINAL_VIDEO, JSON_DB])

def run_insert_fingerprints():
    if not os.path.exists(JSON_DB):
        print(f"Error: JSON DB '{JSON_DB}' not found! Run build first.")
        return
    print("Inserting fingerprints into SQLite DB...")
    subprocess.run(["python", "insert_fingerprints.py"])

def run_check_clip():
    if not os.path.exists(SQLITE_DB):
        print(f"Error: SQLite DB '{SQLITE_DB}' not found! Run insert first.")
        return
    if not os.path.exists(SUSPECT_VIDEO):
        print(f"Error: Suspect video '{SUSPECT_VIDEO}' not found!")
        return
    print("Checking suspect video for piracy...")
    subprocess.run(["python", "check_clip.py"])

def run_full_pipeline():
    run_build_fingerprint()
    run_insert_fingerprints()
    run_check_clip()

def main():
    print(" enter your choice FOR Content Piracy Detection System")
    
    print("1 Run full pipeline")
    print("2 Exit")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
       run_full_pipeline();
    elif choice == "2":
        print("Exiting...")
    else:
        print("Invalid choice! Try again.")
        main()

if __name__ == "__main__":
    main()