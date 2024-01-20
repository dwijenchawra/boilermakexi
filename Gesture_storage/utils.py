import yaml
import os
import json

current_name = os.path.dirname(os.path.abspath(__file__))


def load_config():
    path = os.path.join(current_name, "../config.yaml")
    with open(path, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config


config = load_config()


def save_dict_as_json(data, path):
    path = os.path.join(config["project_path"], path)
    with open(path, 'w') as f:
        json.dump(data, f)


def load_json(relative_path):
    path = os.path.join(config["project_path"], relative_path)
    with open(path) as f:
        data = json.load(f)
    return data
