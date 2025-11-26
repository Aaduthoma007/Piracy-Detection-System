Hey there,
# Content Piracy Detection System

A simple Python project to detect pirated copies of videos using frame hashing.

## How does  this system works

1. **Original Movie Processing (Fingerprint Creation)**  
   - Take the official/original video.  
   - Extract frames (e.g., every 1 second).  
   - Convert each frame into a hash using `ImageHash`.  
   - Store these hashes in a database (`fingerprints.db`) or JSON file (`original_db.json`).  

2. **Suspect Video Processing (Piracy Check)**  
   - Take a video from YouTube, Telegram, or any platform.  
   - Extract frames in the same way and hash them.  
   - Compare the hashes with the original database.  

3. **Detection**  
   - If many frames from the suspect video match the original → pirated copy.  
   - If few or no frames match → original content.  

> ⚠️ **Bro,Note:** This system only works with the original video file you provide.  


## Installation

1. Clone the repository:

git clone https://github.com/Aaduthoma007/Piracy-Detection-System.git
cd Piracy-Detection-System
python -m venv ContentPiracy
2))))))))))Create and activate a virtual environment:
.\ContentPiracy\Scripts\Activate.ps1  # Windows PowerShell
# or use `source ContentPiracy/bin/activate` on Linux/Mac
3)))))))Install required packages:

pip install opencv-python Pillow imagehash numpy

License
MIT License
