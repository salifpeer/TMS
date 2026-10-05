from uuid import uuid4
from fastapi import HTTPException
from repository.Register import load_employees, save_employees


def register_employee_service(employee):

    employee_data = employee.model_dump(mode="json")

    employees = load_employees()

    # Check if email already exists
    email = employee_data["email"].strip().lower()

    for emp in employees.values():
        if emp["email"].strip().lower() == email:
            raise HTTPException(
                status_code=400,
                detail="An account with this email already exists."
            )

    # Generate employee ID
    employee_id = str(uuid4())
    employee_data["employee_id"] = employee_id

    # Save employee
    employees[employee_id] = employee_data

    save_employees(employees)

    return {
        "message": "Employee registered successfully",
        "employee": employee_data
    }