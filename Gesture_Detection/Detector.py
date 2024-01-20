# gesture detector
from Pose_storage.utils import *
from enum import Enum
from collections import deque


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
    def __init__(self, time_delta, camera_width, camera_height):
        self.q = deque(maxlen=time_delta)
        self.rotation = Rotation.N_A
        self.translation = Translation.N_A
        self.depth = ZDirection.N_A
        self.idle = False
        self.time_delta = time_delta
        self.camera_width = camera_width
        self.camera_height = camera_height
        # plot a rectangle for the points

    def get_min_side_length(self, x_len, y_len):
        return min(x_len / self.camera_width, y_len / self.camera_height)

    def is_clockwise(self):
        # points is your list (or array) of 2d points.
        # (x2 − x1)(y2 + y1)
        s = 0.0
        for i in range(len(self.q) - 1):
            p1 = self.q[i]
            p2 = self.q[i + 1]
            s += (p2["x"] - p1["x"]) * (p2["y"] - p1["y"])

        return s > 0.0

    def update_state(self, point):
        self.rotation = Rotation.N_A
        self.idle = False
        self.translation = Translation.N_A
        self.depth = ZDirection.N_A
        self.q.append(point)
        if len(self.q) < self.time_delta:
            return

        # first determin general shape through points
        # coordinates wrt to the screen
        x_val = []
        y_val = []
        for p in self.q:
            x_val.append(p["x"])
            y_val.append(p["y"])
        min_x, max_x = min(x_val), max(x_val)
        min_y, max_y = min(y_val), max(y_val)
        d_x = max_x - min_x
        d_y = max_y - min_y

        # look at rectangle
        if d_y / d_x >= config["linear_bound"]:
            if self.q[0]["y"] < self.q[-1]["y"]:
                # moving up
                self.translation = Translation.UP
            else:
                self.translation = Translation.DOWN
        elif d_x / d_y >= config["linear_bound"]:
            if self.q[0]["x"] < self.q[-1]["x"]:
                # moving right
                self.translation = Translation.RIGHT
            else:
                self.translation = Translation.LEFT
        else:
            # is in circular shape
            if self.get_min_side_length(d_x, d_y) < config["min_side_len"]:
        # is in idle state
                self.idle = True
            else:
                if self.is_clockwise():
                    self.rotation = Rotation.CW
                else:
                    self.rotation = Rotation.CCW

                # is in circle shape
                # need to determine if ccw or cw


        # now have a box for the description of motion
