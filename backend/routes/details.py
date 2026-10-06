from fastapi import APIRouter, Depends
from services import details
from auth.auth import verify_token
 
router = APIRouter(
    dependencies=[Depends(verify_token)]
)


@router.get("/details")
def get_employee_details(employee_id: str):
    
    return details.get_employee_details(employee_id)