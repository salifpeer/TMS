from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from datetime import date
from uuid import uuid4


# Create router
router = APIRouter(
    prefix="/register",
    tags=["Registration"]
)


# =========================================================
# Pydantic Model / Validation
# =========================================================

class EmployeeRegistration(BaseModel):

    # Automatically generated unique ID
    employee_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: str

    date_of_birth: date

    gender: str = Field(
        min_length=1
    )

    marital_status: str = Field(
        min_length=1
    )

    nationality: str = Field(
        min_length=2,
        max_length=50
    )

    mobile: str

    alternate_mobile: str

    present_address: str = Field(
        min_length=5,
        max_length=300
    )


    # -----------------------------------------------------
    # Email validation
    # -----------------------------------------------------

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):

        if (
            "@" not in value
            or "." not in value
            or value.startswith("@")
            or value.endswith("@")
        ):
            raise ValueError("Please enter a valid email address.")

        return value


    # -----------------------------------------------------
    # Mobile number validation
    # -----------------------------------------------------

    @field_validator("mobile", "alternate_mobile")
    @classmethod
    def validate_mobile(cls, value):

        if not value.isdigit():
            raise ValueError(
                "Mobile number must contain only digits."
            )

        if len(value) != 10:
            raise ValueError(
                "Mobile number must contain exactly 10 digits."
            )

        return value


# =========================================================
# Registration Route
# =========================================================

@router.post("/")
def register_employee(employee: EmployeeRegistration):

    # Later, this route will call the service layer.
    # Example:
    #
    # return register_employee_service(employee)

    return {
        "message": "Employee registration request received",
        "employee": employee
    }