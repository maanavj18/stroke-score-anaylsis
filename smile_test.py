from base_test import BaseTest
from calculations import face_position

class SmileTest(BaseTest):

    SMILE_DURATION = 4
    COUNTDOWN_TIME = 3

    #This number is not tuned
    ASYMMETRY_THRESHOLD = 0.1

    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.status = "WAITING"
        self.score = "INCOMPLETE"
        self.countdown_start = None
        self.start_time = None
        self.max_asymmetry = 0.0
        self.last_print = -1
        self.base_ec_left = None
        self.base_ec_right = None
        self.base_mc_left = None
        self.base_mc_right = None
    
    def get_score(self):
        return self.score
    
    def is_complete(self):
        return self.status == "COMPLETE"
    
    def get_status(self):
        return self.status

    def update(self, buffer):
        status = self.status

        latest = buffer.get_latest()
        if latest is None or latest.face_landmarks is None:
            return
        landmark = latest.face_landmarks

        match status:
            case "WAITING":
                self.status = "COUNTDOWN"
                self.countdown_start = latest.timestamp
                print("COUNTDOWN STARTING\n")

            case "COUNTDOWN":
                time_elapsed = latest.timestamp - self.countdown_start
                current_second = self.COUNTDOWN_TIME - int(time_elapsed)
                
                if current_second != self.last_print and current_second > 0:
                    print(f"{current_second}\n")
                    self.last_print = current_second

                elif time_elapsed >= self.COUNTDOWN_TIME:
                    print("SMILE\n")
                    self.status = "SMILING"
                    self.start_time = latest.timestamp
                    self.base_mc_left = face_position(landmark, 61)
                    self.base_mc_right = face_position(landmark, 291)
                    self.base_ec_left = face_position(landmark, 130)
                    self.base_ec_right = face_position(landmark, 359)
                    
                
            case "SMILING":
                time_elapsed = latest.timestamp - self.start_time

                if time_elapsed <= self.SMILE_DURATION:
                    current_mc_left = face_position(landmark, 61)
                    current_mc_right = face_position(landmark, 291)
                    current_ec_left = face_position(landmark, 130)
                    current_ec_right = face_position(landmark, 359)

                    base_left_diff = self.base_mc_left[1] - self.base_ec_left[1]
                    base_right_diff = self.base_mc_right[1] - self.base_ec_right[1]
                    base_diff = base_left_diff - base_right_diff

                    current_left_diff = current_mc_left[1] - current_ec_left[1]
                    current_right_diff = current_mc_right[1] - current_ec_right[1]
                    current_diff = current_left_diff - current_right_diff

                    asymmetry = abs(current_diff - base_diff)
                    
                    if asymmetry >= self.max_asymmetry:
                        self.max_asymmetry = asymmetry

                elif self.max_asymmetry <= self.ASYMMETRY_THRESHOLD:
                    self.score = "PASS"
                    self.status = "COMPLETE"

                else:
                    self.score = "FAIL"
                    self.status = "COMPLETE"
                
            case "COMPLETE":
                pass

            case _ :
                pass

        