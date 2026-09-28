from fastapi import APIRouter
from services import details

router = APIRouter()
@router.get("/details")
def get_employee_details(employee_id: str):
    
    return details.get_employee_details(employee_id)