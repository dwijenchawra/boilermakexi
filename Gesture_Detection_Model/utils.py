import torch.nn as nn
from Gesture_storage.utils import *
config = load_config()
def load_MLP(output_classes: config["output_classes"]):
    model = nn.Sequential()
    model.add_module("dense1", nn.Linear(21 * 2, 40))
    model.add_module("act1", nn.ReLU())
    model.add_module("drop1", nn.Dropout(p=0.1))
    model.add_module("dense2", nn.Linear(40, 20))
    model.add_module("act2", nn.ReLU())
    model.add_module("drop2", nn.Dropout(p=0.1))
    model.add_module("output", nn.Linear(20, output_classes))
    model.add_module("output_act", nn.Softmax(dim=1))
    return model