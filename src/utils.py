import os
import json

def save_to_json(data: dict, filename: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_from_json(filename: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', filename)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
