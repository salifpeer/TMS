from uuid import uuid4
from fastapi import HTTPException
from repository.Register import (
    load_employees,
    save_employees
)


def register_employee_service(employee):

    employee_data = employee.model_dump(mode="json")

    employees = load_employees()

    # Handle backward compatibility if database was loaded as a list
    if isinstance(employees, list):
        emp_dict = {}
        for emp in employees:
            if isinstance(emp, dict):
                emp_id = emp.get("employee_id", str(uuid4()))
                emp["employee_id"] = emp_id
                emp_dict[emp_id] = emp
        employees = emp_dict

    new_email = employee_data.get("email", "").strip().lower()
    for existing_emp in employees.values():
        if isinstance(existing_emp, dict) and existing_emp.get("email", "").strip().lower() == new_email:
            raise HTTPException(
                status_code=400,
                detail="An account with this email address already exists."
            )

    employee_id = str(uuid4())
    employee_data["employee_id"] = employee_id

    employees[employee_id] = employee_data

    save_employees(employees)

    return {
        "message": "Employee registered successfully",
        "employee": employee_data
    }