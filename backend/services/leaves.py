from datetime import datetime

from repository.leaves import load_leaves, save_leaves


def apply_leave(employee_id, start_date, end_date, reason):

    leaves = load_leaves()

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if end < start:
        return {
            "message": "Ending date cannot be before starting date"
        }

    total_leave_days = (end - start).days + 1

    if employee_id not in leaves:
        leaves[employee_id] = []

    leave = {
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
        "total_leave_days": total_leave_days
    }

    leaves[employee_id].append(leave)

    save_leaves(leaves)

    return {
        "message": "Leave applied successfully",
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
        "total_leave_days": total_leave_days
    }


def get_leaves(employee_id):

    leaves = load_leaves()

    if employee_id not in leaves:
        return []

    return leaves[employee_id]