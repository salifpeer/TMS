from fastapi import APIRouter
from pydantic import BaseModel

from services.attendance import check_in, get_attendance


router = APIRouter(prefix="/attendance", tags=["attendance"])


class CheckInRequest(BaseModel):
    employee_id: str
    employee_name: str


@router.post("/checkin")
def checkin(request: CheckInRequest) -> dict:
    return check_in(request.employee_id, request.employee_name)


@router.get("")
def attendance_records() -> list[dict]:
    return get_attendance()
