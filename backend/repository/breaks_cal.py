import json
from datetime import datetime

file = "break_in_out.json"


def break_in(employee_id):

    with open(file, "r") as file:
        data = json.load(file)

    if employee_id not in data:
        data[employee_id] = {
            "break_in_times": [],
            "break_out_times": []
        }

    break_in_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    data[employee_id]["break_in_times"].append(break_in_time)

    with open(file, "w") as file:
        json.dump(data, file, indent=4)

    print("Break started at:", break_in_time)


def resume_work(employee_id):

    with open(file, "r") as file:
        data = json.load(file)

    break_out_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    data[employee_id]["break_out_times"].append(break_out_time)

    with open(file, "w") as file:
        json.dump(data, file, indent=4)

    print("Work resumed at:", break_out_time)


def calculate_total_break_time(employee_id):

    with open(file, "r") as file:
        data = json.load(file)

    break_in_times = data[employee_id]["break_in_times"]
    break_out_times = data[employee_id]["break_out_times"]

    total_break_time = 0

    for i in range(len(break_in_times)):

        start_time = datetime.strptime(break_in_times[i], "%d-%b-%Y %H:%M:%S") #because json frile return string value 
        

        end_time = datetime.strptime(break_out_times[i],"%d-%b-%Y %H:%M:%S"
        )

        break_duration = end_time - start_time

        total_break_time = break_duration + total_break_time

    return total_break_time