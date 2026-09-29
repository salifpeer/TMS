import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field

from backend.services.auth import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Tells FastAPI to look for the "Authorization: Bearer <token>" header and
# also gives us the Authorize button in the /docs page.
bearer_scheme = HTTPBearer(auto_error=False)


# --- request / response models -------------------------------------------
class LoginRequest(BaseModel):
    """
    Whatever the client posts is checked against this first.

    If the email is not a real email, or the password is empty, FastAPI
    answers 422 on its own and our function is never called.
    """

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class UserResponse(BaseModel):
    email: EmailStr
    name: str


# --- dependency used by protected routes ----------------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    Read the bearer token, verify it, and hand back who the caller is.

    Any route that adds this as a dependency becomes a protected route.
    """
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired, please sign in again",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise unauthorized

    email = payload.get("sub")
    if not email:
        raise unauthorized

    return {"email": email, "name": payload.get("name", "")}


# --- routes ---------------------------------------------------------------
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest):
    """Check the credentials and hand back a JWT if they are correct."""
    user = authenticate_user(payload.email, payload.password)

    if user is None:
        # Same answer for a wrong password and an email that does not exist.
        # Telling them apart would let anyone test which emails are registered.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(email=user["email"], name=user["name"])

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)):
    """
    Protected route. Without a valid token this answers 401.

    The dashboard calls it on load, which is what stops somebody from opening
    the dashboard page without signing in.
    """
    return UserResponse(email=current_user["email"], name=current_user["name"])
