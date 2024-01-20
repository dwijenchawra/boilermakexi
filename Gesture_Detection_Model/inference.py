import numpy as np
import torch
from Gesture_Detection_Model.utils import *
from Gesture_storage.utils import *
import copy
import itertools

import numpy as np

config = load_config()


def pre_process_landmark(landmark_list):
    tmp = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(tmp):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        tmp[index][0] = tmp[index][0] - base_x
        tmp[index][1] = tmp[index][1] - base_y

    # Convert to a one-dimensional list
    tmp = list(
        itertools.chain.from_iterable(tmp))

    # Normalization
    max_value = max(list(map(abs, tmp)))

    def normalize_(n):
        return n / max_value

    tmp = list(map(normalize_, tmp))

    return tmp


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    for _, landmark in enumerate(landmarks.landmark):
        x = min(int(landmark.x * image_width), image_width - 1)
        y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([x, y])

    return landmark_point


class MLP_Inference(object):
    def __init__(self, threads=1, output_classes=config["output_classes"]):
        self.model = torch.load(config["model_save_path"])
        torch.set_num_threads(int(threads))

    def __call__(
            self,
            landmark_list,
    ):
        inp = torch.tensor(landmark_list, dtype=torch.float32)
        inp = inp.unsqueeze(0)
        out = self.model(inp)
        out = out.squeeze(0)
        return np.argmax(np.squeeze(out.detach().numpy()))
