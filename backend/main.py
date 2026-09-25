from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.Register import router


# Create FastAPI application
app = FastAPI(
    title="Employee Management System",
    description="Employee registration and management API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include Registration Router
app.include_router(router)


# Home route
@app.get("/")
def home():
    return {
        "message": "Employee Management API is running"
    }