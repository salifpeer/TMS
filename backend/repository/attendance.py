import json

path = "database/attendance.json"


def load_attendance():

    with open(path, "r") as file:
        data = json.load(file)

    return data


def save_attendance(data):

    with open(path, "w") as file:
        json.dump(data, file, indent=4)