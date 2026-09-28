from fastapi import FastAPI
from routes.Register import router


# Create FastAPI application
app = FastAPI(
    title="Employee Management System",
    description="Employee registration and management API",
    version="1.0.0"
)


# Include Registration Router
app.include_router(router)


