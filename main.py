import cv2
import numpy as np
import mediapipe as mp
from vision import VisionLayer
from frame_buffer import FrameBuffer


def main():
    vision = VisionLayer()
    vision.start()
    
    buffer = FrameBuffer()

    print("Vision layer started. Press q to quit.")

    last_display = None  # hold last valid frame

    while True:
        frame_data = vision.get_latest_frame()

        if frame_data is not None and frame_data.raw_frame is not None:
            last_display = frame_data.raw_frame.copy()
            buffer.add(frame_data)
            if frame_data.timestamp % 3 <= 0.033:
                window = buffer.get_window(5)
                print(f"Buffer size: {len(window)} frames | oldest: {round(window[0].timestamp % 100, 2)} | newest: {round(window[-1].timestamp % 100, 2)}")

            pose  = "YES" if frame_data.pose_landmarks is not None else "NO"
            face  = "YES" if frame_data.face_landmarks is not None else "NO"
            lhand = "YES" if frame_data.left_hand is not None else "NO"
            rhand = "YES" if frame_data.right_hand is not None else "NO"
            #print(f"pose: {pose} | face: {face} | left_hand: {lhand} | right_hand: {rhand}")

            if frame_data.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    last_display,
                    frame_data.pose_landmarks,
                    mp.solutions.holistic.POSE_CONNECTIONS
                )

        if last_display is not None:
            cv2.imshow("Vision Layer Test", last_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vision.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()