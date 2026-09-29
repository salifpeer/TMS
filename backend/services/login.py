from fastapi import HTTPException

from pydantic import BaseModel, EmailStr
from repository.login import get_user
from auth.auth import create_token


class LoginData(BaseModel):

    email: EmailStr
    password: str
def login_user(data: LoginData):

    
    user = get_user(
        data.email
    )

    
    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    
    if user["password"] != data.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    token = create_token(
        data.email
    )

    # Return response
    return {
        "access_token": token,

        "status_code": 200,

        "user": {
            "employee_id": user["employee_id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "date_of_birth": user["date_of_birth"],
            "gender": user["gender"],
            "marital_status": user["marital_status"],
            "nationality": user["nationality"],
            "mobile": user["mobile"],
            "alternate_mobile": user["alternate_mobile"],
            "present_address": user["present_address"]
        }
    }