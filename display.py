import mediapipe as mp

class Renderer:

    def __init__(self,):
        self.width = 640
        self.height = 480

    
    def draw(self,frame, frame_data, test):
        self._draw_pose(frame, frame_data)
        self._draw_face_landmarks(frame, frame_data)
        self._draw_status(frame, test)
        self._draw_timer(frame, test)
        self._draw_result(frame, test)
        return frame


    def _draw_pose(self, frame, frame_data):
        pass

    def _draw_face_landmarks(self, frame, frame_data):
        pass

    def _draw_status(self, frame, test):
        pass

    def _draw_timer(self, frame, test):
        pass

    def _draw_result(self, frame, test):
        pass