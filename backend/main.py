from fastapi import FastAPI
from routes.attendance import router as attendance_router
app = FastAPI()
app.include_router(attendance_router)