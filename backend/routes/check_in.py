from fastapi import APIRouter
  
from services import attendance
from fastapi import APIRouter, Depends
 
from auth.auth import verify_token
 
router = APIRouter(
    dependencies=[(verify_token)]
)

@router.post("/checkin")
def checkin(employee_id: str):
 
    return attendance.checkin(employee_id)
 