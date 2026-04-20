from base_test import BaseTest
import calculations

class SmileTest(BaseTest):

    DURATION = 4
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
                current_second = int(latest.timestamp - self.countdown_start)
                if current_second != self.last_print and current_second > 0:
                    print(f"{current_second}")

                    if current_second >= self.COUNTDOWN_TIME:
                        self.status = "SMILING"
                        self.start_time = latest.timestamp
                
            case "SMILING":
                pass
            case "COMPLETE":
                pass
            case _ :
                pass

        