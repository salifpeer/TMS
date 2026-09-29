import os

import requests
import streamlit as st


FRONTEND_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LOGO_PATH = os.path.join(
    FRONTEND_DIR,
    "logo.png"
)


API_URL = "http://127.0.0.1:8000"


def login():

    if os.path.exists(LOGO_PATH):

        st.image(
            LOGO_PATH,
            width=150
        )

    st.title("Sign In")

    email = st.text_input(
        "Email Address"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Sign In",
        type="primary"
    ):

        if email.strip() == "" or password == "":

            st.error(
                "Please fill in all fields!"
            )

            return

        try:

            response = requests.post(
                f"{API_URL}/login",
                json={
                    "email": email.strip(),
                    "password": password
                }
            )

        except requests.exceptions.RequestException:

            st.error(
                "Could not connect to the backend."
            )

            return

        if response.status_code == 200:

            data = response.json()

            
            token = data["access_token"]

            
            user = data["user"]
            st.write(f"Welcome, {user['full_name']}!")


        elif response.status_code == 401:

            st.error(
                "Invalid email or password!"
            )

        elif response.status_code == 422:

            st.error(
                "Invalid request data!"
            )

        else:

            st.error(
                f"Login failed: {response.status_code}"
            )


if "page" not in st.session_state:

    st.session_state["page"] = "login"


if st.session_state["page"] == "login":

    login()