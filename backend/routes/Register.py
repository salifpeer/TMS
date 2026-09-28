from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from datetime import date
from services.registerservice import register_employee_service


router = APIRouter(
    prefix="/register",
    tags=["Registration"]
)


class EmployeeRegistration(BaseModel):

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

    password: str

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


@router.post("/employee")
def register_employee(employee: EmployeeRegistration):
    return register_employee_service(employee)
