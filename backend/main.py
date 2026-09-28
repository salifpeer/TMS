from fastapi import FastAPI
from routes.attendance import router as attendance_router
from routes.leaves import router as leaves_router
from routes.details import router as details_router
from routes.Register import router as register_router
from backend.routes.mehar_routes import router as auth_router


app = FastAPI(
    title="TMS Authentication API",
    description="Login and JWT issuing for the TMS project.",
    version="1.0.0",
)

app.include_router(attendance_router)
app.include_router(leaves_router)
app.include_router(details_router)
app.include_router(register_router)



# Every route inside mehar_routes.py already carries the /auth prefix,
# so the login endpoint ends up at POST /auth/login.
app.include_router(auth_router)


@app.get("/", tags=["Health"])
def health():
    """Quick way to check the server is up."""
    return {"status": "ok", "service": "TMS Authentication API"}

