from base_test import BaseTest
from calculations import avg_position, joint_angle, distance, position, velocity, vertical_diff

class ArmTest(BaseTest):

    DURATION = 10
    DRIFT_THRESHOLD = 0.15
    DROP_THRESHOLD = 0.2
    STRAIGHT_ARM_THRESHOLD = 160
    HORIZONTAL_THRESHOLD = 0.1


    def __init__(self):
        self.reset()
        

    def reset(self):
        self.status = "WAITING"
        self.score = "INCOMPLETE"
        self.start_time = None
        self.baseline_left = None
        self.baseline_right = None
        self.max_drift_diff = 0.0

    
    def update(self, buffer):
        status = self.get_status()
        window = buffer.get_window(2)

        if status == "WAITING":
            latest = buffer.get_latest()
            if latest is None or latest.pose_world_landmarks is None:
                return
            landmark = latest.pose_world_landmarks

            
            shoulderL = position(landmark, 11)
            shoulderR = position(landmark, 12)
            elbowL = position(landmark, 13)
            elbowR = position(landmark, 14)
            wristL = position(landmark, 15)
            wristR = position(landmark, 16)

            check1 = vertical_diff(wristL, wristR) <= self.HORIZONTAL_THRESHOLD
            check2 = (vertical_diff(wristL, shoulderL) <= self.HORIZONTAL_THRESHOLD) and (vertical_diff(wristR, shoulderR) <= self.HORIZONTAL_THRESHOLD)
            check3 = (joint_angle(wristL, elbowL, shoulderL) >= self.STRAIGHT_ARM_THRESHOLD) and (joint_angle(wristR, elbowR, shoulderR) >= self.STRAIGHT_ARM_THRESHOLD)

            if check1 and check2 and check3:
                self.status = "RUNNING"
                self.start_time = latest.timestamp
                self.baseline_left = wristL[1]
                self.baseline_right = wristR[1]
            
            

            
        elif status == "RUNNING":
            latest = buffer.get_latest()
            if latest is None or latest.pose_world_landmarks is None:
                return
            landmark = latest.pose_world_landmarks
            
            checkTime = latest.timestamp - self.start_time >= self.DURATION
            checkFall = None
    


        else:
            return
        

    
    def get_score(self):
        return self.score

    
    def is_complete(self):
        return self.status == "COMPLETE"

    
    def get_status(self):
        return self.status

