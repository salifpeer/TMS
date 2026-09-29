import os
import json


USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json") ###here


def load_users() -> list:
    """Read every user record from the JSON file."""
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("users", [])


def find_user_by_email(email: str):
    """Find one user by email, or None. Email match is case insensitive."""
    email = email.strip().lower()

    for user in load_users():
        if user["email"].lower() == email:
            return user

    return None
