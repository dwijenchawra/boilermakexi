import torch.nn as nn
from Hand_Tracking.Pose_storage.utils import *
config = load_config()
def load_MLP():
    global config
    config = load_config()
    model = nn.Sequential()
    model.add_module("dense1", nn.Linear(21 * 2, 64))
    model.add_module("act1", nn.ReLU())
    model.add_module("drop1", nn.Dropout(p=0.2))
    model.add_module("dense2", nn.Linear(64, 32))
    model.add_module("act2", nn.ReLU())
    model.add_module("drop2", nn.Dropout(p=0.2))
    model.add_module("output", nn.Linear(32, config["output_classes"]))
    model.add_module("output_act", nn.Softmax(dim=1))
    return model