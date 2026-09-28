from fastapi import APIRouter
from pydantic import BaseModel

from services import leaves


router = APIRouter()


class LeaveRequest(BaseModel):
    employee_id: str
    start_date: str
    end_date: str
    reason: str


@router.post("/leave")
def apply_leave(data: LeaveRequest):

    return leaves.apply_leave(
        data.employee_id,
        data.start_date,
        data.end_date,
        data.reason
    )


@router.get("/leaves")
def get_leaves(employee_id: str):

    return leaves.get_leaves(employee_id)