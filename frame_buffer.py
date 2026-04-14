import collections
import threading

class FrameBuffer:
    def __init__(self, max_seconds=5):
        # stores frames, owns the lock
        self.frames = collections.deque()
        self.max_seconds = max_seconds
        self.lock = threading.Lock()

    def add(self, frame_data):
        with self.lock:
            self.frames.append(frame_data)

            #Removes old data from buffer
            current_time = frame_data.timestamp
            while len(self.frames) > 1 and current_time - self.frames[0].timestamp >= self.max_seconds:
                self.frames.popleft()

    def get_window(self, seconds):
        # returns list of FrameData from the last N seconds
        # this is what evaluation modules call
        with self.lock:
            if not self.frames:
                return []
            
            current_time = self.frames[-1].timestamp
            threshold_time = current_time - seconds
            
            return [f for f in self.frames if f.timestamp >= threshold_time]

    def get_latest(self):
        # returns the single most recent FrameData
        # useful for the display layer
        with self.lock:
            if self.frames:
                return self.frames[-1]
            return None