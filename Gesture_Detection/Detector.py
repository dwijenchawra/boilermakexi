# gesture detector
from Pose_storage.utils import *
from enum import Enum
from queue import Queue
class ZDirection(Enum):
    INTO_SCREEN = 0
    OUT_OF_SCREEN = 1
    N_A = 2

class Rotation(Enum):
   N_A = 0
   CCW = 1
   CW = 2

class Translation(Enum):
    N_A = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    RIGHT = 4


config = load_config()


class Detector:
    def __init__(self, time_delta):
        self.q = Queue(maxsize=time_delta)
        self.rotation = Rotation.N_A
        self.translation = Translation.N_A
        self.depth = ZDirection.N_A
        # plot a rectangle for the points





