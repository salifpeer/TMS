from fastapi import FastAPI

from backend.routes.mehar_routes import router as auth_router

app = FastAPI(
    title="TMS Authentication API",
    description="Login and JWT issuing for the TMS project.",
    version="1.0.0",
)


app.include_router(auth_router)


@app.get("/", tags=["Health"])
def health():
    """Quick way to check the server is up."""
    return {"status": "ok", "service": "TMS Authentication API"}
