# gesture detector
from Pose_storage.utils import *
from enum import Enum
from queue import Queue
class ZDirection(Enum):
    INTO_SCREEN = 0
    OUT_OF_SCREEN = 1
    N_A = 2

class Rotation(Enum):

   CCW = 0
   CW = 1
class Color(Enum):
    N_A = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    RIGHT = 4
    INTO_SCREEN = 5
    OUT_OF_SCREEN = 6


config = load_config()

class Detector:
    def __init__(self, time_delta):
        self.q = Queue(maxsize=time_delta)
        # plot a rectangle for the points





