import os
import cv2
import imagehash
from PIL import Image
import sqlite3

# configurationnnnnnn
SUSPECT_VIDEO = "suspect.mp4"
DB_FILE = "fingerprints.db"
FRAME_INTERVAL = 1        # seconds
HASH_THRESHOLD = 5        # max Hamming distance to consider "match"
PIRACY_PERCENTAGE = 30    # % of matching frames to flag as piracy

# for checking if theere is a video
if not os.path.isfile(SUSPECT_VIDEO):
    raise FileNotFoundError(f"Suspect video '{SUSPECT_VIDEO}' not found!")

# fingerprint loading from sqllite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("SELECT frame_time, frame_hash FROM movie_fingerprints WHERE source = ?", ("original.mp4",))
original_frames = cursor.fetchall()
conn.close()

if not original_frames:
    raise ValueError("No fingerprints found in the database for original.mp4!")

# Convert hash strings to imagehash objects
original_hashes = [(time, imagehash.hex_to_hash(h)) for time, h in original_frames]

#  Open suspect video ---
cap = cv2.VideoCapture(SUSPECT_VIDEO)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if fps == 0:
    raise ValueError("FPS is 0. Cannot process video. Check the file path and format.")

duration = frame_count / fps
matched = 0
total_checked = 0
sec = 0

print(f"Checking: {SUSPECT_VIDEO}")

while sec < duration:
    cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    frame_hash = imagehash.phash(pil_img)

    # Compare with all original hashes
    for _, orig_hash in original_hashes:
        if frame_hash - orig_hash <= HASH_THRESHOLD:
            matched += 1
            break

    total_checked += 1
    sec += FRAME_INTERVAL

cap.release()

# --- Result --hope this works
match_percentage = (matched / total_checked) * 100 if total_checked > 0 else 0
print(f"Matched frames: {matched}/{total_checked} -> {match_percentage:.2f}%")
if match_percentage > PIRACY_PERCENTAGE:
    print("🚨 PIRACY DETECTED")
else:
    print("U R OG and its Not detected as pirated")
