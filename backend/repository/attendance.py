import json

FILE_PATH = "database/attendance.json"


def load_attendance():

    with open(FILE_PATH, "r") as file:
        data = json.load(file)

    return data


def save_attendance(data):

    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)