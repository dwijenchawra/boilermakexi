import numpy as np
import torch
from Gesture_Detection_Model.utils import *
from Gesture_storage.utils import *

config = load_config()


class MLP_Inference(object):
    def __init__(self, threads=1, output_classes=config["output_classes"]):
        self.model = load_MLP(output_classes)
        self.model.load_state_dict(torch.load(config["model_save_path"]))
        torch.set_num_threads(threads)

    def __call__(
            self,
            landmark_list,
    ):
        inp = torch.tensor(landmark_list, dtype=torch.float32)
        out = self.model(inp)
        return np.argmax(np.squeeze(out))
