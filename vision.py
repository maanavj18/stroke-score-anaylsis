import cv2
import mediapipe as mp
import time
from dataclasses import dataclass, field
import threading
import queue

@dataclass
class FrameData:
    raw_frame: any = None


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
        try:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW is the Windows-specific backend
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            if not cap.isOpened():
                print("Error: Could not open webcam.")
                return

            time.sleep(0.5)

            while not self._stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break
                timestamp = time.time()

                try:
                    self.capture_queue.put_nowait((timestamp, frame))
                except queue.Full:
                    pass

            cap.release()
        except Exception as e:
            print(f"CaptureThread crashed: {e}")


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

        try:
            
            while not self._stop_event.is_set():
                try:
                    (timestamp, frame) = self.capture_queue.get(timeout=0.1)
                except queue.Empty:
                    print("Q empty")
                    continue

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame.flags.writeable = False
                results = self.model.process(rgb_frame)
                rgb_frame.flags.writeable = True

                
                left_hand = results.left_hand_landmarks
                right_hand = results.right_hand_landmarks

                frame_data = FrameData(
                    raw_frame = frame,
                    timestamp = timestamp,
                    pose_landmarks = results.pose_landmarks,
                    pose_world_landmarks = results.pose_world_landmarks,
                    face_landmarks = results.face_landmarks,
                    left_hand = left_hand,
                    right_hand = right_hand
                )

                try:
                    self.output_queue.put_nowait(frame_data)
                except queue.Full:
                    print("Q full inf")
                    pass
            
            self.model.close()
        except Exception as e:
            print(f"InferenceThread crashed: {e}")



class VisionLayer:
    def __init__(self):
        self.capture_queue = queue.Queue(maxsize =4)
        self.output_queue = queue.Queue(maxsize =4)
        
        self.capture_thread = CaptureThread(self.capture_queue)
        self.inference_thread = InferenceThread(self.capture_queue, self.output_queue)


    def start(self):
        self.capture_thread.start()
        self.inference_thread.start()

    
    def get_latest_frame(self):
        
        try:
            return self.output_queue.get_nowait()
        except queue.Empty:
            return None
    
    
    def stop(self):
        self.capture_thread.stop()
        self.inference_thread.stop()
        self.capture_thread.join()
        self.inference_thread.join()




        





