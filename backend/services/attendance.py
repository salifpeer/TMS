from datetime import datetime, timedelta
 
from repository.attendance import load_attendance, save_attendance
 
from Location_based_check_in import check_location

 
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
    if check_location() is True:
        data = load_attendance()
    
        employee = get_employee(data, employee_id)
    
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
            "break_time": "0:00:00",
            "working_time": "-"
        }
    else:
        return {"message":"The employee isn't within the office range"}
        
 
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
 
    # Check if already on break
 
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
            "checkin_time": employee["checkin"],
            "checkout_time": employee["checkout"] or "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }
 
    # Check if already resumed
 
    if len(employee["break_starts"]) == len(employee["break_resumes"]):
 
        return {
            "message": "You are not on break",
            "status": employee["status"],
            "checkin_time": employee["checkin"],
            "checkout_time": employee["checkout"] or "-",
            "break_time": employee["break_duration"],
            "working_time": "-"
        }
 
    # Add resume time
 
    employee["break_resumes"].append(get_current_time())
 
    # Get latest break start
 
    start = datetime.strptime(
        employee["break_starts"][-1],
        TIME_FORMAT
    )
 
    # Get latest break resume
 
    resume = datetime.strptime(
        employee["break_resumes"][-1],
        TIME_FORMAT
    )
 
    # Calculate this break
 
    duration = resume - start
 
    # Get previous total break duration
 
    old_duration = datetime.strptime(
        employee["break_duration"],
        "%H:%M:%S"
    )
 
    # Convert old duration to timedelta
 
    old_duration = timedelta(
        hours=old_duration.hour,
        minutes=old_duration.minute,
        seconds=old_duration.second
    )
 
    # Add new break to previous break
 
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
    if check_location is False:
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
    
        # Cannot checkout while on break
    
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
    
        checkin = datetime.strptime(
            employee["checkin"],
            TIME_FORMAT
        )
    
        checkout = datetime.strptime(
            employee["checkout"],
            TIME_FORMAT
        )
    
        # Total time
    
        total_time = checkout - checkin
    
        # Break duration
    
        break_duration = datetime.strptime(
            employee["break_duration"],
            "%H:%M:%S"
        )
    
        break_duration = timedelta(
            hours=break_duration.hour,
            minutes=break_duration.minute,
            seconds=break_duration.second
        )
    
        # Working time
    
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
    else:
        return {"message":"The employee isn't within the office range "}
    
 
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