import json
def load_details():
    with open("database/details.json", "r") as file:
        data = json.load(file)

    return data
def save_details(data):
    with open("database/details.json", "w") as file:
        json.dump(data, file, indent=4)
    