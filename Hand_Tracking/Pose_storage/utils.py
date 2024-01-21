import yaml
import os
import csv
import json
import pandas as pd

current_name = os.path.dirname(os.path.abspath(__file__))


def remove_id_from_csv(csv_path, id):
    path = os.path.join(config["project_path"], csv_path)
    df = pd.read_csv(f'{path}',header=None)
    df = df[df[0] != id]
    df.reset_index(drop=True, inplace=True)
    df.loc[df[0] > id] -= 1
    df.to_csv(path, index=False)


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


def update_config(data):
    path = os.path.join(current_name, "../config.yaml")
    with open(path, 'w') as f:
        yaml.dump(data, f)


def add_to_csv(data, path):
    path = os.path.join(config["project_path"], path)

    with open(path, 'a') as graphFile:
        graphFileWriter = csv.writer(graphFile)
        for row in data:
            graphFileWriter.writerow(row)
