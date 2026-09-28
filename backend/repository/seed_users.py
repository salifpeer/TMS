"""
Creates users.json with the demo accounts we are testing login against.

Registration is being built by the other team member, so until their API is
ready this script is what puts users in the system. Run it from the project
root:

    python -m backend.repository.seed_users

HASH_PASSWORDS below controls how the passwords are written.

While we are testing it is set to False, so users.json holds short passwords
you can read and type straight away. Flip it to True and re-run the script to
write them as salted hashes instead. Login works either way, because
verify_password handles both formats.
"""

import json

from backend.services.auth import hash_password
from backend.repository.repo import USERS_FILE


HASH_PASSWORDS = False


DEMO_USERS = [
    {"email": "mehr12@gmail.com", "name": "Mehr Ali", "password": "mehr12"},
    {"email": "mehr22@gmail.com", "name": "Mehr Khan", "password": "mehr22"},
    {"email": "mehr33@hotmail.com", "name": "Mehr Fatima", "password": "mehr33"},
]


def seed():
    users = [
        {
            "id": index,
            "email": user["email"],
            "name": user["name"],
            "password": (
                hash_password(user["password"])
                if HASH_PASSWORDS
                else user["password"]
            ),
        }
        for index, user in enumerate(DEMO_USERS, start=1)
    ]

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=2)

    print(f"Wrote {len(users)} users to {USERS_FILE}")
    for user in DEMO_USERS:
        print(f"  {user['email']}  /  {user['password']}")


if __name__ == "__main__":
    seed()
