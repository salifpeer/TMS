import os
import sys

import requests
import streamlit as st

FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)

for _path in (PROJECT_ROOT, FRONTEND_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from backend.api.client import get_current_user  # noqa: E402

LOGO_PATH = os.path.join(FRONTEND_DIR, "logo.png")


def sign_out():
    """Drop the token and go back to the sign in page."""
    st.session_state.pop("token", None)
    st.session_state.pop("email", None)
    st.session_state["page"] = "login"
    st.rerun()


def dashboard():

    token = st.session_state.get("token")

    # Somebody landed here without signing in.
    if not token:
        st.warning("Please sign in first.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    # The page does not trust the session, it asks the API to confirm the
    # token on every load. An expired or edited token gets kicked out here.
    try:
        response = get_current_user(token)
    except requests.exceptions.RequestException:
        st.error("Could not reach the server. Is the backend still running?")
        return

    if response.status_code == 401:
        st.error("Your session has expired. Please sign in again.")
        if st.button("Back to Sign In"):
            sign_out()
        return

    if response.status_code != 200:
        st.error(f"Could not load your profile: {response.status_code}")
        return

    user = response.json()

    st.image(LOGO_PATH, width=150)
    st.title("Dashboard")
    st.success(f"Welcome to the dashboard, {user['email']}")

    st.write("")
    st.write("This is a placeholder page while the real dashboard is built.")

    st.write("")
    if st.button("Sign Out", type="primary"):
        sign_out()
