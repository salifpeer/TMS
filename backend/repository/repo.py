"""
Repository layer: the only place that knows where user data is stored.

Right now that is a JSON file. When the team moves to a real database only
this file changes, the service and the routes stay exactly as they are.
"""

import os
import json

# users.json sits next to this file, so build the path from __file__ instead
# of a relative path. Otherwise it would break depending on the folder the
# server was started from.
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")


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
