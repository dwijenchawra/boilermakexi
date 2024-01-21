import yaml
import os
import csv
import json

# get the directory 4 levels up (project root)
project_root = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(project_root)
hand_tracking_root = project_root
project_root = os.path.dirname(project_root)
project_root = os.path.dirname(project_root)



def load_config():
    path = os.path.join(project_root, "config.yaml")
    with open(path, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config


config = load_config()


def save_dict_as_json(data, path):
    path = os.path.join(hand_tracking_root, path)
    with open(path, 'w') as f:
        json.dump(data, f)


def load_json(relative_path):
    path = os.path.join(hand_tracking_root, relative_path)
    with open(path) as f:
        data = json.load(f)
    return data


def update_config(data):
    path = os.path.join(project_root, "config.yaml")
    with open(path, 'w') as f:
        yaml.dump(data, f)


def add_to_csv(data, path):
    path = os.path.join(config["project_path"], path)

    with open(path, 'a') as graphFile:
        graphFileWriter = csv.writer(graphFile)
        for row in data:
            graphFileWriter.writerow(row)
