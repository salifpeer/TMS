from fastapi import APIRouter

from services import attendance


router = APIRouter()



@router.post("/checkin")
def checkin(employee_id: str):

    return attendance.checkin(employee_id)



@router.post("/checkout")
def checkout(employee_id: str):

    return attendance.checkout(employee_id)



@router.post("/break/start")
def take_break(employee_id: str):

    return attendance.start_break(employee_id)



@router.post("/break/resume")
def resume_break(employee_id: str):

    return attendance.resume_break(employee_id)