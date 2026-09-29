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
