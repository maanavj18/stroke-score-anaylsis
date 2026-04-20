from abc import ABC, abstractmethod
from frame_buffer import FrameBuffer

class BaseTest(ABC):

    @abstractmethod
    def update(self, buffer):
        pass

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def is_complete(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_status(self):
        pass



