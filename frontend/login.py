"""
Sign in page. This is the file you run with streamlit.

    streamlit run frontend/login.py
"""

import os
import re
import sys

import requests
import streamlit as st

FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)

# Put the project root on the import path so "from backend..." works, and this
# folder so the sibling pages import cleanly no matter how the app was started.
for _path in (PROJECT_ROOT, FRONTEND_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from backend.api.client import login  # noqa: E402

from config import REGISTER_URL  # noqa: E402
from dashboard import dashboard  # noqa: E402
from register import register  # noqa: E402


LOGO_PATH = os.path.join(FRONTEND_DIR, "logo.png")


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


def sign_in():

    st.image(LOGO_PATH, width=150)

    st.title("Sign In")

    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Sign In", type="primary"):

        # Checked here first so we do not send an obviously bad request.
        # The API validates the same things again, it never trusts the client.
        if email.strip() == "" or password == "":
            st.error("Please fill in all fields!")
            return

        if not is_valid_email(email.strip()):
            st.error("Please enter a valid email address!")
            return

        try:
            response = login(email.strip(), password)
        except requests.exceptions.RequestException:
            st.error(
                "Could not reach the server. Start the backend first: "
                "uvicorn backend.mehar_main:app --reload"
            )
            return

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state["token"] = token
            st.session_state["email"] = email.strip()
            st.session_state["page"] = "dashboard"

            st.rerun()

        elif response.status_code == 401:
            st.error("Invalid email or password!")

        elif response.status_code == 404:
            st.error("User not found!")

        elif response.status_code == 422:
            st.error("Invalid request data!")

        elif response.status_code == 500:
            st.error("Server error, please try again in a moment.")

        else:
            st.error(f"Request failed: {response.status_code}")


def register_link():
    """
    "Not registered yet" line under the form.

    Once the registration link is filled in inside config.py this becomes a
    real link to your teammate's page. Until then it opens the placeholder.
    """
    if REGISTER_URL.strip():
        st.markdown(
            f"Not registered yet? [Register here]({REGISTER_URL.strip()})",
            unsafe_allow_html=False,
        )
    else:
        st.write("Not registered yet?")
        if st.button("Register here"):
            st.session_state["page"] = "register"
            st.rerun()


if "page" not in st.session_state:
    st.session_state["page"] = "login"


if st.session_state["page"] == "login":

    sign_in()
    register_link()

elif st.session_state["page"] == "register":

    register()

elif st.session_state["page"] == "dashboard":

    dashboard()
