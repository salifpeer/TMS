import json


path = "Database/register.json"


def get_user(email):

    with open(
        path,
        "r"
    ) as file:

        users = json.load(file)

    for employee_id, user in users.items():

        if user["email"] == email:

            return user

    return None