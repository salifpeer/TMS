import json
def load_attendance():
    with open("./Database/attendace.json","r") as f:
        data=json.load(f)
        return data
def save_attendance(data):
    with open("./Database/attendace.json","w") as f:
        json.dump(data,f)
