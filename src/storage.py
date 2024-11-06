import json
import os

from src.config_loader import load_config

DATA_FILE = "posts_data.json"


config = load_config()
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {topic: [] for topic in config["app"]["hot_topics"]}


def save_data(data, n=10):
    data = {topic: data[topic][-n:] for topic in data}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
