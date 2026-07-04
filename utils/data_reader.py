import json
import os

def load_json_data(filename="test_data.json"):
    """
    Loads JSON data from the data/ directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
