import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt algorithm with a secure random salt.
    """
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored bcrypt hash.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
