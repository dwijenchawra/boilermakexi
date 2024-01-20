import math


def init_gesture_from_values(endpoints, score, label):
    d = {"endpoints": endpoints,
         "score": score,
         "label": label}
    return Static_gesture(d)


class Static_gesture():
    def __init__(self, d):
        self.points = d["endpoints"]
        self.score = d["score"]
        self.label = d["label"]

    def xy_distance(self, x, y):
        return math.sqrt((x - self.x)(x - self.x) + (y - self.y) * (y - self.y))

    def get_json_data(self):
        d = {"endpoints": self.points,
             "score": self.score,
             "label": self.label}
        return d
