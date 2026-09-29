from datetime import datetime, timedelta, timezone

from jose import jwt


SECRET_KEY = "abd"

ALGORITHM = "HS256"


def create_token(email):

    expire = (
        datetime.now(timezone.utc)
        + timedelta(hours=1)
    )

    data = {
        "sub": email,
        "exp": expire
    }

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token