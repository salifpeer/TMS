import json
import os

DATABASE_FILE = "./database/register.json"


def load_employees():

    if not os.path.exists(DATABASE_FILE):
        os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
        with open(DATABASE_FILE, "w") as file:
            json.dump([], file)
        return []

    with open(DATABASE_FILE, "r") as file:
        data = json.load(file)

    return data


def save_employees(data):

    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=4)