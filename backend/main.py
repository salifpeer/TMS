from fastapi import FastAPI

from routes.attendance import router as attendance_router


app = FastAPI(title="TMS Attendance API")
app.include_router(attendance_router)
