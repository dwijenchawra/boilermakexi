import math


class Gesture:
    def __init__(self, x, y, z):
        self.y = y
        self.z = z
        self.x = x

    def xy_distance(self, x, y):
        return math.sqrt((x - self.x)(x - self.x) + (y - self.y) * (y - self.y))