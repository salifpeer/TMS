from fastapi import FastAPI
from routes.attendance import router as attendance_router
from routes.leaves import router as leaves_router
from routes.details import router as details_router
from routes.Register import router as register_router
from routes.login import router as login_router

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(attendance_router)
app.include_router(leaves_router)
app.include_router(details_router)
app.include_router(register_router)
app.include_router(login_router)
