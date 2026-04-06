import cv2
import mediapipe as mp
import numpy as np
import os
import time
from dataclasses import dataclass, field
import threading
import queue

@dataclass
class FrameData:
    timestamp : float = 0.0
    pose_landmarks: any = None
    pose_world_landmarks: any = None
    face_landmarks: any = None
    left_hand: any = None
    right_hand: any = None
    visibility_scores: dict = field(default_factory=dict)


class CaptureThread(threading.Thread):
    def __init__(self, capture_queue):
        super().__init__(daemon=True)
        self.capture_queue = capture_queue
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        while not self._stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            timestamp = time.time()

            try:
                self.capture_queue.put_nowait((timestamp, frame))
            except queue.Full:
                print("Warning: Capture queue is full.")
                pass

            

        cap.release()


class InferenceThread(threading.Thread):
    def __init__(self, capture_queue, output_queue):
        super().__init__(daemon=True)
        self.capture_queue = capture_queue
        self.output_queue = output_queue
        self._stop_event = threading.Event()
        self.model = mp.solutions.holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            try:
                (timestamp, frame) = self.capture_queue.get(timeout=0.1)
            except queue.Empty:
                print("Q empty")
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model.process(rgb_frame)

            if results:
                left_hand = results.left_hand_landmarks
                right_hand = results.right_hand_landmarks

                frame_data = FrameData(
                    timestamp = timestamp
                    pose_landmarks = results.pose_landmarks
                    pose_world_landmarks = results.pose_world_landmarks
                    face_landmarks
                )
                








        





