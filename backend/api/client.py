import os

import requests

BASE_URL = os.getenv("TMS_API_URL", "http://127.0.0.1:8000")

# Fail fast instead of leaving the UI spinning if the API is not answering.
TIMEOUT = 10


def login(email: str, password: str) -> requests.Response:
    """POST the credentials. 200 gives back a token, 401 means they are wrong."""
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )


def get_current_user(token: str) -> requests.Response:
    """
    Ask the API who the token belongs to.

    This is the call that makes the dashboard a protected page: no token or a
    bad one and the API answers 401.
    """
    return requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=TIMEOUT,
    )
