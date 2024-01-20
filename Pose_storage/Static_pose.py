import math
from Pose_storage.utils import load_config
from Pose_Detection_Model.inference import *

config = load_config()


def init_pose_from_values(endpoints, score, label, id, parsed_endpoints):
    d = {"endpoints": endpoints,
         "score": score,
         "id": id,
         "parsed_datapoints": parsed_endpoints,
         "label": label}
    return Static_pose(d)


def get_dist(p1, p2):
    return math.sqrt((p1["x"] - p2["x"]) * (p1["x"] - p2["x"]) + (p1["y"] - p2["y"]) * (p1["y"] - p2["y"]))


class Static_pose():
    def __init__(self, d):
        self.points = d["endpoints"]
        self.score = d["score"]
        self.parsed_endpoints = d["parsed_datapoints"]
        self.label = d["label"]
        self.id = d["id"]

    def get_json_data(self):
        d = {"id": self.id,
             "score": self.score,
             "label": self.label,
             "parsed_datapoints": self.parsed_endpoints,
             "endpoints": self.points}
        return d

    def get_rmse_v2(self, g):
        rmse = 0
        weights = config["threshold_weights"]
        for i in range(len(self.points)):
            weight = weights[i]
            rmse += weight * (g.parsed_endpoints[2 * i] - self.parsed_endpoints[2 * i]) * (
                    g.parsed_endpoints[i] - self.parsed_endpoints[i])
            rmse += weight * (g.parsed_endpoints[2 * i + 1] - self.parsed_endpoints[2 * i + 1]) * (
                    g.parsed_endpoints[2 * i + 1] - self.parsed_endpoints[2 * i + 1])
        return rmse / len(self.points)

    def get_rmse(self, g):
        rmse_x = 0.
        rmse_y = 0.
        weights = config["threshold_weights"]
        for i in range(len(self.points)):
            weight = weights[i]
            rmse_x += weight * (g.points[i]["x"] - self.points[i]["x"]) * (g.points[i]["x"] - self.points[i]["x"])
            rmse_y += weight * (g.points[i]["y"] - self.points[i]["y"]) * (g.points[i]["y"] - self.points[i]["y"])
        return rmse_x / len(self.points) + rmse_y / len(self.points)

        # loop over
