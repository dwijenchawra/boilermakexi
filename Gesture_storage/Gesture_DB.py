from Gesture_storage.utils import *
from Gesture_storage.Static_gesture import *

config = load_config()


def load_gestures_from_json(path: config["db_path"]):
    raw_data = load_json(path)
    raw_gestures = raw_data['gestures']
    gestures = [Static_gesture(raw_gesture) for raw_gesture in raw_gestures]
    return gestures


class Gesture_DB:
    def __init__(self, db_path):
        self.gestures = load_gestures_from_json(db_path)
        self.db_path = db_path

    def save_gesture_to_json(self):
        gestures = {"gestures": [gesture.get_json_data() for gesture in self.gestures]}
        save_dict_as_json(gestures, self.db_path)
