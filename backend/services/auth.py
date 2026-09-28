"""
Auth service: password hashing, password checking and JWT tokens.

Everything security related lives here so the routes stay thin and the
repository only has to worry about reading data.
"""

import os
import hmac
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from backend.repository.repo import find_user_by_email


# --- settings -------------------------------------------------------------
# In a real deployment these come from the environment (.env / server config).
# The fallback values are only here so the project runs out of the box.
SECRET_KEY = os.getenv("TMS_SECRET_KEY", "dev-secret-change-me-before-deploy")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TMS_TOKEN_EXPIRE_MINUTES", "30"))

# PBKDF2 settings used when hashing passwords.
PBKDF2_ROUNDS = 260000
STORED_FORMAT = "pbkdf2_sha256${rounds}${salt}${hash}"


# --- password handling ----------------------------------------------------
def hash_password(plain_password: str) -> str:
    """Turn a plain password into a salted hash that is safe to store."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode(), salt.encode(), PBKDF2_ROUNDS
    ).hex()
    return STORED_FORMAT.format(rounds=PBKDF2_ROUNDS, salt=salt, hash=digest)


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Check a typed password against what is stored.

    Two formats are accepted:

      1. A plain password, which is what the demo accounts in users.json use
         while registration is still being built.
      2. A pbkdf2_sha256 hash, which is what registration will write.

    Keeping both means login keeps working on the day the other half of the
    task lands, without anybody having to touch this file.
    """
    if not stored_password.startswith("pbkdf2_sha256$"):
        return hmac.compare_digest(plain_password, stored_password)

    try:
        algorithm, rounds, salt, expected = stored_password.split("$")
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    digest = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode(), salt.encode(), int(rounds)
    ).hex()

    # compare_digest instead of == so the comparison time does not leak
    # information about how much of the hash matched.
    return hmac.compare_digest(digest, expected)


# --- JWT ------------------------------------------------------------------
def create_access_token(email: str, name: str) -> str:
    """Build a signed token that proves who the caller is."""
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": email,        # subject: who the token belongs to
        "name": name,
        "iat": issued_at,    # issued at
        "exp": expires_at,   # expiry, PyJWT rejects the token after this
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Read a token back.

    Raises jwt.ExpiredSignatureError if it is past its expiry and
    jwt.InvalidTokenError if the signature or the shape is wrong.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# --- login use case -------------------------------------------------------
def authenticate_user(email: str, password: str):
    """
    Return the user record when the email and password match, otherwise None.

    The caller decides what error to raise. We deliberately do not tell the
    difference between "no such email" and "wrong password" so nobody can use
    the login form to find out which emails are registered.
    """
    user = find_user_by_email(email)
    if user is None:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user
