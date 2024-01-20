from Gesture_storage.utils import *
from Gesture_storage.Gesture import *


def load_gestures_from_json(db_path):
    raw_data = load_json(db_path)
    raw_gestures = raw_data['gestures']
    gestures = [Gesture(raw_gesture) for raw_gesture in raw_gestures]
    return gestures


class Gesture_DB:
    def __init__(self, db_path):
        self.gesture_db = load_gestures_from_json(db_path)
