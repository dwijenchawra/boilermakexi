import math


def init_gesture_from_values(endpoints, score, label, id):
    d = {"endpoints": endpoints,
         "score": score,
         "id": id,
         "label": label}
    return Static_gesture(d)


def get_dist(p1, p2):
    return math.sqrt((p1["x"] - p2["x"]) * (p1["x"] - p2["x"]) + (p1["y"] - p2["y"]) * (p1["y"] - p2["y"]))


class Static_gesture():
    def __init__(self, d):
        self.points = d["endpoints"]
        self.score = d["score"]
        self.label = d["label"]
        self.id = d["id"]

    def get_json_data(self):
        d = {"id": self.id,
             "score": self.score,
             "label": self.label,
             "endpoints": self.points}
        return d

    def get_rmse(self, g):
        all_dist = 0.
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = g.points[i]
            all_dist += get_dist(p1, p2)
        return all_dist / len(self.points)

        # loop over
