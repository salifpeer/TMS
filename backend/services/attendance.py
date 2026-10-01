from datetime import datetime, timedelta
from fastapi import HTTPException

from repository.attendance import load_attendance, save_attendance
from services.Location_based_check_in import check_location


TIME_FORMAT = "%d-%b-%Y %I:%M:%S %p"


def get_current_time():
    return datetime.now().strftime(TIME_FORMAT)


def get_today():
    return datetime.now().strftime("%d-%b-%Y")


def get_employee(data, employee_id):

    today = get_today()

    if employee_id not in data:
        data[employee_id] = {}

    if today not in data[employee_id]:
        data[employee_id][today] = {
            "status": "Not Checked In",
            "checkin": "",
            "checkout": "",
            "break_starts": [],
            "break_resumes": [],
            "break_duration": "0:00:00",
            "working_time": ""
        }

    return data[employee_id][today]


# CHECK IN

def checkin(employee_id):

    data = load_attendance()

    employee = get_employee(data, employee_id)

    if check_location() is not True:

        raise HTTPException(
            status_code=400,
            detail="The employee isn't within the office range"
        )

    if employee["checkin"]:

        return {
            "message": "Already checked in",
            "status": employee["status"],
            "checkin_time": employee["checkin"],
            "checkout_time": employee["checkout"] or "-",
            "break_time": employee["break_duration"],
            "working_time": employee["working_time"] or "-"
        }

    employee["checkin"] = get_current_time()
    employee["status"] = "Checked In"

    save_attendance(data)

    return {
        "message": "Checked in successfully",
        "status": employee["status"],
        "checkin_time": employee["checkin"],
        "checkout_time": "-",
        "break_time": employee["break_duration"],
        "working_time": "-"
    }


# START BREAK

def start_break(employee_id):

    data = load_attendance()

    employee = get_employee(data, employee_id)

    if not employee["checkin"]:

        return {
            "message": "Please check in first",
            "status": employee["status"],
            "checkin_time": "-",
            "checkout_time": "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }

    if employee["checkout"]:

        return {
            "message": "Already checked out",
            "status": employee["status"],
            "checkin_time": employee["checkin"],
            "checkout_time": employee["checkout"],
            "break_time": employee["break_duration"],
            "working_time": employee["working_time"]
        }

    if len(employee["break_starts"]) > len(employee["break_resumes"]):

        return {
            "message": "Already on break",
            "status": employee["status"],
            "checkin_time": employee["checkin"],
            "checkout_time": "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }

    employee["break_starts"].append(get_current_time())

    employee["status"] = "On Break"

    save_attendance(data)

    return {
        "message": "Break started",
        "status": employee["status"],
        "checkin_time": employee["checkin"],
        "checkout_time": "-",
        "break_time": employee["break_duration"],
        "working_time": "-"
    }


# RESUME BREAK

def resume_break(employee_id):

    data = load_attendance()

    employee = get_employee(data, employee_id)

    if not employee["break_starts"]:

        return {
            "message": "You are not on break",
            "status": employee["status"],
            "checkin_time": employee["checkin"] or "-",
            "checkout_time": employee["checkout"] or "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }

    if len(employee["break_starts"]) == len(employee["break_resumes"]):

        return {
            "message": "You are not on break",
            "status": employee["status"],
            "checkin_time": employee["checkin"] or "-",
            "checkout_time": employee["checkout"] or "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }

    employee["break_resumes"].append(get_current_time())

    start = datetime.strptime(
        employee["break_starts"][-1],
        TIME_FORMAT
    )

    resume = datetime.strptime(
        employee["break_resumes"][-1],
        TIME_FORMAT
    )

    duration = resume - start

    old_duration = datetime.strptime(
        employee["break_duration"],
        "%H:%M:%S"
    )

    old_duration = timedelta(
        hours=old_duration.hour,
        minutes=old_duration.minute,
        seconds=old_duration.second
    )

    break_duration = old_duration + duration

    employee["break_duration"] = str(break_duration)
    employee["status"] = "Checked In"

    save_attendance(data)

    return {
        "message": "Break resumed successfully",
        "status": employee["status"],
        "checkin_time": employee["checkin"],
        "checkout_time": employee["checkout"] or "-",
        "break_time": employee["break_duration"],
        "working_time": "-"
    }


# CHECK OUT

def checkout(employee_id):

    data = load_attendance()

    employee = get_employee(data, employee_id)

    if check_location() is not True:

        raise HTTPException(
            status_code=400,
            detail="The employee isn't within the office range"
        )

    if not employee["checkin"]:

        return {
            "message": "Please check in first",
            "status": employee["status"],
            "checkin_time": "-",
            "checkout_time": "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }

    if employee["checkout"]:

        return {
            "message": "Already checked out",
            "status": employee["status"],
            "checkin_time": employee["checkin"],
            "checkout_time": employee["checkout"],
            "break_time": employee["break_duration"],
            "working_time": employee["working_time"]
        }

    if len(employee["break_starts"]) > len(employee["break_resumes"]):

        return {
            "message": "Please resume your break first",
            "status": employee["status"],
            "checkin_time": employee["checkin"],
            "checkout_time": "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }

    employee["checkout"] = get_current_time()

    checkin_time = datetime.strptime(
        employee["checkin"],
        TIME_FORMAT
    )

    checkout_time = datetime.strptime(
        employee["checkout"],
        TIME_FORMAT
    )

    total_time = checkout_time - checkin_time

    break_duration = datetime.strptime(
        employee["break_duration"],
        "%H:%M:%S"
    )

    break_duration = timedelta(
        hours=break_duration.hour,
        minutes=break_duration.minute,
        seconds=break_duration.second
    )

    working_time = total_time - break_duration
    
    employee["working_time"] = str(working_time)
    employee["status"] = "Checked Out"

    save_attendance(data)

    return {
        "message": "Checked out successfully",
        "status": employee["status"],
        "checkin_time": employee["checkin"],
        "checkout_time": employee["checkout"],
        "break_time": employee["break_duration"],
        "working_time": employee["working_time"]
    }


# GET ATTENDANCE


def get_attendance(employee_id):
 
    data = load_attendance()

    employee = get_employee(data, employee_id)

    return {
        "status": employee["status"],
        "checkin_time": employee["checkin"] or "-",
        "checkout_time": employee["checkout"] or "-",
        "break_time": employee["break_duration"],
        "working_time": employee["working_time"] or "-"
    }