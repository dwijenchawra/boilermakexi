from Pose_storage.utils import *
from Pose_storage.Static_pose import *

config = load_config()


def load_pose_from_json(path: config["db_path"]):
    raw_data = load_json(path)
    raw_pose = raw_data['poses']
    poses = [Static_pose(pose) for pose in raw_pose]
    return poses


class Pose_DB:
    def __init__(self, db_path):
        self.poses = load_pose_from_json(db_path)
        self.db_path = db_path

    def save_pose_to_json(self):
        pose = {"poses": [p.get_json_data() for p in self.poses]}
        save_dict_as_json(pose, self.db_path)

    def add_static_pose(self, static_pose):
        min_id = self.match(static_pose, min_rmse=config["add_threshold"])
        if min_id == "n/a":
            static_pose.id = f"pose_{len(self.poses)}"
            self.poses.append(static_pose)
            self.save_pose_to_json()
            return True
        else:
            return False

    def match(self, pose, min_rmse=config["match_threshold"]):
        min_id = 'n/a'
        for g in self.poses:
            # rmse = g.get_rmse(pose)
            rmse = g.get_rmse_v2(pose)
            print(rmse)
            if rmse < min_rmse:
                min_rmse = rmse
                min_id = g.id
        return min_id
