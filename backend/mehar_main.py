"""
Entry point for the API.

Start it from the project root with:

    uvicorn backend.mehar_main:app --reload

Then open http://127.0.0.1:8000/docs to try the endpoints by hand.
"""

from fastapi import FastAPI

from backend.routes.mehar_routes import router as auth_router

app = FastAPI(
    title="TMS Authentication API",
    description="Login and JWT issuing for the TMS project.",
    version="1.0.0",
)

# Every route inside mehar_routes.py already carries the /auth prefix,
# so the login endpoint ends up at POST /auth/login.
app.include_router(auth_router)


@app.get("/", tags=["Health"])
def health():
    """Quick way to check the server is up."""
    return {"status": "ok", "service": "TMS Authentication API"}
