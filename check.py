import cv2
import imagehash
from PIL import Image
import numpy as np

print("✅ OpenCV version:", cv2.__version__)
print("✅ NumPy version:", np.__version__)
print("✅ ImageHash test:", imagehash.average_hash(Image.new("RGB", (8, 8), color="red")))
