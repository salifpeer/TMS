from datetime import datetime, timedelta

from repository.attendance import load_attendance, save_attendance


TIME_FORMAT = "%d-%b-%Y %I:%M:%S %p"


def get_current_time():
    return datetime.now().strftime(TIME_FORMAT)


def checkin(employee_id):

    data = load_attendance()

    employee = data[employee_id]

    # Already checked in
    if employee["checkins"]:

        return {
            "message": "You have already checked in",
            "status": employee["status"],
            "checkin_time": employee["checkins"][0],
            "checkout_time": (
                employee["checkouts"][0]
                if employee["checkouts"]
                else "-"
            )
        }

    current_time = get_current_time()

    employee["checkins"].append(current_time)
    employee["status"] = "Checked In"

    save_attendance(data)

    return {
        "message": "Checked in successfully",
        "status": employee["status"],
        "checkin_time": current_time,
        "checkout_time": "-"
    }


def checkout(employee_id):

    data = load_attendance()

    employee = data[employee_id]

    # Employee has not checked in
    if not employee["checkins"]:

        return {
            "message": "Please check in first",
            "status": employee["status"],
            "checkin_time": "-",
            "checkout_time": "-"
        }

    # Employee has already checked out
    if employee["checkouts"]:

        return {
            "message": "You have already checked out",
            "status": employee["status"],
            "checkin_time": employee["checkins"][0],
            "checkout_time": employee["checkouts"][0]
        }

    
    if len(employee["break_starts"]) > len(employee["break_resumes"]):

        return {
            "message": "Please resume your break first",
            "status": employee["status"],
            "checkin_time": employee["checkins"][0],
            "checkout_time": "-"
        }

    current_time = get_current_time()

    checkin_time = datetime.strptime(
        employee["checkins"][0],
        TIME_FORMAT
    )

    checkout_time = datetime.strptime(
        current_time,
        TIME_FORMAT
    )

    total_time = checkout_time - checkin_time

    total_break = timedelta()

    for start, end in zip(
        employee["break_starts"],
        employee["break_resumes"]
    ):

        start_time = datetime.strptime(
            start,
            TIME_FORMAT
        )

        end_time = datetime.strptime(
            end,
            TIME_FORMAT
        )

        total_break += end_time - start_time

    total_working = total_time - total_break

    employee["checkouts"].append(current_time)

    employee["status"] = "Checked Out"

    employee["total_break_time"] = str(total_break)

    employee["total_working_time"] = str(total_working)

    save_attendance(data)

    return {
        "message": "Checked out successfully",
        "status": employee["status"],
        "checkin_time": employee["checkins"][0],
        "checkout_time": current_time,
        "total_break_time": str(total_break),
        "total_working_time": str(total_working)
    }


def start_break(employee_id):

    data = load_attendance()

    employee = data[employee_id]

    # Employee has not checked in
    if not employee["checkins"]:

        return {
            "message": "Please check in first",
            "status": employee["status"],
            "checkin_time": "-",
            "checkout_time": "-"
        }

    # Employee has already checked out
    if employee["checkouts"]:

        return {
            "message": "You have already checked out",
            "status": employee["status"],
            "checkin_time": employee["checkins"][0],
            "checkout_time": employee["checkouts"][0]
        }

    # Employee is already on break
    if len(employee["break_starts"]) > len(employee["break_resumes"]):

        return {
            "message": "You are already on break",
            "status": employee["status"],
            "checkin_time": employee["checkins"][0],
            "checkout_time": "-"
        }

    current_time = get_current_time()

    employee["break_starts"].append(current_time)

    employee["status"] = "On Break"

    save_attendance(data)

    return {
        "message": "Break started",
        "status": employee["status"],
        "checkin_time": employee["checkins"][0],
        "checkout_time": "-",
        "break_start": current_time
    }


def resume_break(employee_id):

    data = load_attendance()

    employee = data[employee_id]

    # Employee is not on break
    if len(employee["break_starts"]) == len(employee["break_resumes"]):

        return {
            "message": "You are not currently on break",
            "status": employee["status"],
            "checkin_time": employee["checkins"][0]
            if employee["checkins"]
            else "-",
            "checkout_time": employee["checkouts"][0]
            if employee["checkouts"]
            else "-"
        }

    current_time = get_current_time()

    break_start = datetime.strptime(
        employee["break_starts"][-1],
        TIME_FORMAT
    )

    break_end = datetime.strptime(
        current_time,
        TIME_FORMAT
    )

    break_duration = break_end - break_start

    employee["break_resumes"].append(current_time)

    employee["status"] = "Checked In"

    total_break = timedelta()

    for start, end in zip(
        employee["break_starts"],
        employee["break_resumes"]
    ):

        start_time = datetime.strptime(
            start,
            TIME_FORMAT
        )

        end_time = datetime.strptime(
            end,
            TIME_FORMAT
        )

        total_break += end_time - start_time

    employee["total_break_time"] = str(total_break)

    save_attendance(data)

    return {
        "message": "Break resumed successfully",
        "status": employee["status"],
        "checkin_time": employee["checkins"][0],
        "checkout_time": (
            employee["checkouts"][0]
            if employee["checkouts"]
            else "-"
        ),
        "break_resume": current_time,
        "break_duration": str(break_duration),
        "total_break_time": str(total_break)
    }


