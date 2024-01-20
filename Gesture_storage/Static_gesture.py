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
        rmse_x = 0.
        rmse_y = 0.
        for i in range(len(self.points)):
            rmse_x += (g.points[i]["x"] - self.points[i]["x"]) * (g.points[i]["x"] - self.points[i]["x"])
            rmse_y += (g.points[i]["y"] - self.points[i]["y"]) * (g.points[i]["y"] - self.points[i]["y"])
        return sum([rmse_x / len(self.points), rmse_y / len(self.points)]) / 2

        # loop over
