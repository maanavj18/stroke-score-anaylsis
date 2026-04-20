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
    
    def get_score(self):
        return self.score
    
    def is_complete(self):
        return self.status == "COMPLETE"
    
    def get_status(self):
        return self.status

    def update(self, buffer):
        status = self.status

        match status:
            case "WAITING":
                pass
            case "COUNTDOWN_START":
                pass
            case "SMILING":
                pass
            case "COMPLETE":
                pass

        pass