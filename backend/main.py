from fastapi import FastAPI
from routes.attendance import router as attendance_router
from routes.leaves import router as leaves_router
from routes.details import router as details_router
from routes.Register import router as register_router

app = FastAPI()
app.include_router(attendance_router)
app.include_router(leaves_router)
app.include_router(details_router)
app.include_router(register_router)
