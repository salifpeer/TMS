from repository.details import load_details, save_details
def get_employee_details(employee_id):
    details = load_details()

    if employee_id not in details:
        return {
            "message": "Employee not found"
        }

    return details[employee_id]