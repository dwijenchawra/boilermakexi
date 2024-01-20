# gesture detector
from Hand_Tracking.Pose_storage.utils import *
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


def get_min_side_length(x_len, y_len, camera_width, camera_height):
    return min(camera_width / x_len, camera_height / y_len)


class Detector:
    def __init__(self, time_delta):
        self.q = deque(maxlen=time_delta)
        self.rotation = Rotation.N_A
        self.translation = Translation.N_A
        self.depth = ZDirection.N_A
        self.idle = False
        self.time_delta = time_delta
        # plot a rectangle for the points

    def get_state(self):
        depth_state = self.depth.name
        if self.rotation != Rotation.N_A:
            return self.rotation.name, depth_state

        if self.translation != Translation.N_A:
            return self.translation.name, depth_state

        if self.rotation != Rotation.N_A:
            return self.translation.name, depth_state

        if self.idle:
            return "idle", self.depth.name

        return "n/a"

    def is_clockwise(self):
        # points is your list (or array) of 2d points.
        # (x2 − x1)(y2 + y1)
        s = 0.0
        for i in range(len(self.q) - 1):
            p1 = self.q[i]
            p2 = self.q[i + 1]
            s += (p2["x"] - p1["x"]) * (p2["y"] - p1["y"])

        return s > 0.0

    def polygonArea(self):
        area = 0.
        for i in range(len(self.q)):
            j = (i + 1) % len(self.q)
            area += self.q[i]["x"] * self.q[j]["y"]
            area -= self.q[j]["x"] * self.q[i]["y"]
        return area

    def update_state(self, point, camera_height, camera_width):
        self.rotation = Rotation.N_A
        self.idle = False
        self.translation = Translation.N_A
        self.depth = ZDirection.N_A
        if point is None:
            self.q.popleft()
            return
        self.q.append(point)
        if len(self.q) < self.time_delta:
            return

        z_delta = self.q[-1]["z"] - self.q[0]["z"]
        print(z_delta)
        if z_delta < - config["zoom_thresh"]:
            self.depth = ZDirection.INTO_SCREEN
        elif z_delta > config["zoom_thresh"]:
            self.depth = ZDirection.OUT_OF_SCREEN

        # first determine general shape through points
        x_val = []
        y_val = []
        for p in self.q:
            x_val.append(p["x"])
            y_val.append(p["y"])
        min_x, max_x = min(x_val), max(x_val)
        min_y, max_y = min(y_val), max(y_val)
        d_x = max_x - min_x
        d_y = max_y - min_y

        # first see if even to consider motion
        min_side_length = get_min_side_length(d_x, d_y, camera_width, camera_height)
        if min_side_length > config["min_side_len_ratio"]:
            # is in idle state
            self.idle = True
            return
        # look at rectangle
        if d_y / max(d_x, 0.1) >= config["linear_bound"]:
            if self.q[0]["y"] < self.q[-1]["y"]:
                # moving up
                self.translation = Translation.DOWN
            else:
                self.translation = Translation.UP
        elif d_x / max(d_y, 0.1) >= config["linear_bound"]:
            if self.q[0]["x"] < self.q[-1]["x"]:
                # moving right
                self.translation = Translation.LEFT
            else:
                self.translation = Translation.RIGHT
        else:
            # is in circular shape
            print("min LEN: ", min_side_length)
            if min_side_length > config["min_side_len_ratio"]:
                # is in idle state
                self.idle = True
            else:
                if self.polygonArea() > 0:
                    self.rotation = Rotation.CCW
                else:
                    self.rotation = Rotation.CW
