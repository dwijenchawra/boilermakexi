import yaml
import os
import json

config = yaml.safe_load("../config.yaml")

def load_json(relative_path):
    path = os.path.join(config["project_path"],relative_path)
    with open(path) as f:
        data = json.load(f)
    return data