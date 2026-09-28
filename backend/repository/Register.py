import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_FILE = os.path.join(BASE_DIR, "Database", "register.json")


def load_employees():
    if not os.path.exists(DATABASE_FILE):
        os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
        with open(DATABASE_FILE, "w") as file:
            json.dump({}, file)
        return {}

    with open(DATABASE_FILE, "r") as file:
        try:
            data = json.load(file)
        except Exception:
            data = {}

    return data


def save_employees(data):
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=4)