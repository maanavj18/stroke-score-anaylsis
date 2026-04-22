from threading import currentThread
from base_test import BaseTest
from calculations import  joint_angle, position, vertical_diff, face_position, is_visible

class ArmTest(BaseTest):

    DURATION = 10
    DRIFT_THRESHOLD = 0.15
    DROP_THRESHOLD = 0.2
    STRAIGHT_ARM_THRESHOLD = 140
    HORIZONTAL_THRESHOLD = 0.2
    EYE_CLOSED_THRESHOLD = 0.02


    def __init__(self):
        self.reset()
        

    def reset(self):
        self.status = "WAITING"
        self.score = "INCOMPLETE"
        self.start_time = None
        self.baseline_left = None
        self.baseline_right = None
        self.max_drift_diff = 0.0
        self.last_eye_warning = 0.0
        self.wait_run_pause = None
        self.diagnostic_timer = 0.0


    def get_score(self):
        return self.score

    
    def is_complete(self):
        return self.status == "COMPLETE"

    
    def get_status(self):
        return self.status
        
    
    def update(self, buffer):
        status = self.get_status()
        latest = buffer.get_latest()
        current_time = latest.timestamp

        if latest is None or latest.pose_world_landmarks is None or latest.face_landmarks is None:
            return
        landmark = latest.pose_world_landmarks
        face_landmark = latest.face_landmarks

        eyeLU = face_position(face_landmark, 159)
        eyeLL = face_position(face_landmark, 145)
        eyeRU = face_position(face_landmark, 386)
        eyeRL = face_position(face_landmark, 374)

        eyeLDiff = abs(eyeLL[1] - eyeLU[1])
        eyeRDiff = abs(eyeRL[1] - eyeRU[1])

        eyeCheck = eyeLDiff <= self.EYE_CLOSED_THRESHOLD and eyeRDiff <= self.EYE_CLOSED_THRESHOLD


        match status:
            case "WAITING":
                # check all required landmarks are actually visible
                required = [11, 12, 13, 14, 15, 16]
                if not all(is_visible(landmark, i) for i in required):
                    if current_time % 2 <= 0.033:
                        print("NOT VISIBLE")
                    return

                shoulderL = position(landmark, 11)
                shoulderR = position(landmark, 12)
                elbowL = position(landmark, 13)
                elbowR = position(landmark, 14)
                wristL = position(landmark, 15)
                wristR = position(landmark, 16)
                
                #Check to make sure 
                check_wrist_level = vertical_diff(wristL, wristR) <= self.HORIZONTAL_THRESHOLD
                check_shoulder_wrist = (vertical_diff(wristL, shoulderL) <= self.HORIZONTAL_THRESHOLD) and (vertical_diff(wristR, shoulderR) <= self.HORIZONTAL_THRESHOLD)
                check_straight = (joint_angle(wristL, elbowL, shoulderL) >= self.STRAIGHT_ARM_THRESHOLD) and (joint_angle(wristR, elbowR, shoulderR) >= self.STRAIGHT_ARM_THRESHOLD)

                ##############  DEBUGGING CODE  #############################
                shoulder_wrist_diff = vertical_diff(wristL, shoulderL)

                if current_time - self.diagnostic_timer >= 1:
                    self.diagnostic_timer = current_time
                    print(f"Shoulder/Wrist Y Diff: {shoulder_wrist_diff:.4f}")
                    #print(f"check_wrist_level: {check_wrist_level} | check_shoulder_wrist: {check_shoulder_wrist} | check_straight: {check_straight} | eyes: {eyeCheck}")
                    #print(f"eyeL: {eyeLDiff:.4f} | eyeR: {eyeRDiff:.4f}")
                    #print(f"wristDiff: {vertical_diff(wristL, wristR):.4f} | wristLShoulder: {vertical_diff(wristL, shoulderL):.4f} | wristRShoulder: {vertical_diff(wristR, shoulderR):.4f}")
                    #print(f"angleL: {joint_angle(wristL, elbowL, shoulderL):.1f} | angleR: {joint_angle(wristR, elbowR, shoulderR):.1f}")
                
                #########################################################

                #Commented out to make sure that Waiting is the only stage
                '''
                if check_wrist_level and check_straight and eyeCheck:
                    if self.wait_run_pause is None:
                        self.wait_run_pause = current_time
                    elif current_time - self.wait_run_pause >=1: 
                        self.status = "RUNNING"
                        self.start_time = current_time
                        self.baseline_left = wristL[1]
                        self.baseline_right = wristR[1]
                else:
                    self.wait_run_pause = None
                
                '''

            case "RUNNING":

                if not eyeCheck and current_time - self.last_eye_warning >= 1:
                    print("Warning: eyes are open\n")
                    self.last_eye_warning = current_time

                wristL = position(landmark, 15)
                wristR = position(landmark, 16)
            
                leftDrift = wristL[1] - self.baseline_left
                rightDrift = wristR[1] - self.baseline_right
                LRDrift = abs(leftDrift - rightDrift)

                if LRDrift >= self.max_drift_diff:
                    self.max_drift_diff = LRDrift

                checkTime = current_time - self.start_time >= self.DURATION
                checkEarlyDrop = abs(leftDrift) <= self.DROP_THRESHOLD and abs(rightDrift) <= self.DROP_THRESHOLD

                 #########DEBUG##############
                if current_time % 3 <= 0.033:
                    wristL_debug = position(landmark, 15)
                    wristR_debug = position(landmark, 16)
                    leftDrift_debug = wristL_debug[1] - self.baseline_left
                    rightDrift_debug = wristR_debug[1] - self.baseline_right
                    print(f"leftDrift: {leftDrift_debug:.4f} | rightDrift: {rightDrift_debug:.4f} | baseline_left: {self.baseline_left:.4f} | baseline_right: {self.baseline_right:.4f}")
                
                    print(f"checkEarlyDrop: {checkEarlyDrop} | LRDrift: {LRDrift:.4f} | max_drift_diff: {self.max_drift_diff:.4f}")
                ##############################################################

                if not checkEarlyDrop:
                    self.score = "FAIL"
                    self.status = "COMPLETE"
                    return
            
                if checkTime:
                    if self.max_drift_diff <= self.DRIFT_THRESHOLD:
                        self.score = "PASS"
                    else:
                        self.score = "FAIL"
                    
                    self.status = "COMPLETE"

                    return
                
                


            case _:
                return

