import sqlite3
import json

# Open the JSON fingerprint database
with open("original_db.json", "r") as f:
    data = json.load(f)

# Connect to SQLite (or create the DB if it doesn't exist)
conn = sqlite3.connect("fingerprints.db")
cursor = conn.cursor()

# Create the table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS movie_fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    frame_time REAL,
    frame_hash TEXT
)
""")

# Insert each frame's hash
for frame in data["frame_hashes"]:
    cursor.execute(
        "INSERT INTO movie_fingerprints (source, frame_time, frame_hash) VALUES (?, ?, ?)",
        (data["source"], frame["time"], frame["hash"])
    )

# Commit and close
conn.commit()
conn.close()

print("Inserted all fingerprints into fingerprints.db")
