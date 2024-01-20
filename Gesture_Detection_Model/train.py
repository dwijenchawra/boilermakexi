import numpy as np
import torch
from Gesture_storage.utils import *
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from Gesture_Detection_Model.utils import *
import torch.nn as nn

RANDOM_SEED = 42
config = load_config()

dataset = os.path.join(config["project_path"], config["dataset_path"])
model_save_path = config["model_save_path"]
output_classes = config["output_classes"]

x = np.loadtxt(dataset, delimiter=',', dtype='float32',
               usecols=list(range(1, (21 * 2) + 1)))

y = np.loadtxt(dataset, delimiter=',', dtype='long', usecols=(0))
print(x.shape)
print(y.shape)

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.75, shuffle=True)
train_loader = DataLoader(list(zip(x_train, y_train)), shuffle=True, batch_size=128)
valid_loader = DataLoader(list(zip(x_test, y_test)), shuffle=True, batch_size=128)


print(next(enumerate(train_loader)))

model = load_MLP(config["output_classes"])
print(model)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
net_train_loss = []
net_valid_loss = []

for n in range(config["epochs"]):
    model.training = True
    for i, (x, y) in enumerate(train_loader):
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    net_train_loss.append(loss.item())

    model.training = False
    with torch.no_grad():
        for i, (x, y) in enumerate(valid_loader):
            y_pred = model(x)
            loss = loss_fn(y_pred, y)
    net_valid_loss.append(loss.item())
    # early stopping
    min_steps = config["min_train_steps"]
    if len(net_valid_loss) > min_steps * 2:
        prev_avg = sum(net_valid_loss[- 2 * min_steps: - min_steps]) / min_steps
        curr_avg = sum(net_valid_loss[- min_steps:]) / min_steps
        # print(f"current avg: {curr_avg}, previous avg: {prev_avg}")
        if prev_avg - curr_avg < config["break_early"]:
            print("breaking bc of early stopping")
            break

plt.plot(net_train_loss, label="train")
plt.plot(net_valid_loss, label="valid")
plt.show()
path = os.path.join(config["project_path"], config["model_save_path"])
torch.save(model, path)