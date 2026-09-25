from fastapi import HTTPException
from repository.registerrepo import (
    load_employees,
    save_employees
)


def register_employee_service(employee):

    # Convert Pydantic model into dictionary
    employee_data = employee.model_dump(mode="json")

    # Load existing employees
    employees = load_employees()

    # Check if email already exists
    new_email = employee_data.get("email", "").strip().lower()
    for existing_emp in employees:
        if existing_emp.get("email", "").strip().lower() == new_email:
            raise HTTPException(
                status_code=400,
                detail="An account with this email address already exists."
            )

    # Add new employee
    employees.append(employee_data)

    # Save updated employee list
    save_employees(employees)

    # Return response
    return {
        "message": "Employee registered successfully",
        "employee": employee_data
    }