import cv2
import mediapipe as mp
import numpy as np

print(f"OpenCV: {cv2.__version__}")
print(f"MediaPipe: {mp.__version__}")
print(f"NumPy: {np.__version__}")

# Quick camera check
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    print(f"Camera OK — frame shape: {frame.shape}")
else:
    print("Camera FAILED — check your webcam connection")
cap.release()