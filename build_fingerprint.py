
import sys
import cv2
import imagehash
from PIL import Image
import json
import numpy as np
import os

SAMPLE_SECONDS = 1  # sample one frame every 1 second
HASH_FUNC = imagehash.average_hash  # or imagehash.phash

def extract_frame_hashes(video_path, sample_seconds=SAMPLE_SECONDS):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration = total_frames / fps if fps else 0

    hashes = []
    sec = 0
    while sec < duration:
        frame_no = int(sec * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()
        if not ret:
            break
        # convert BGR (cv2) -> RGB (PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        h = HASH_FUNC(pil_img)
        hashes.append({"time": float(sec), "hash": str(h)})
        sec += sample_seconds

    cap.release()
    return hashes

def main():
    if len(sys.argv) < 3:
        print("Usage: python build_fingerprint.py original_movie.mp4 output_db.json")
        return

    video_path = sys.argv[1]
    out_json = sys.argv[2]

    if not os.path.exists(video_path):
        print("Video file not found:", video_path)
        return

    print("Processing:", video_path)
    hashes = extract_frame_hashes(video_path, SAMPLE_SECONDS)
    db = {
        "source": os.path.basename(video_path),
        "sample_seconds": SAMPLE_SECONDS,
        "hash_size": 8,  # default for average_hash
        "frame_hashes": hashes
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
    print(f"Saved fingerprint DB to {out_json} ({len(hashes)} frames).")

if __name__ == "__main__":
    main()
