"""
Placeholder registration page.

Registration belongs to the other team member. This file only exists so the
"Register here" link has somewhere to go while their page is not available.
Replace this whole file with theirs when it is ready, keeping a function
called register() so login.py can still call it.
"""

import os

import streamlit as st

from config import REGISTER_URL

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")


def register():

    st.image(LOGO_PATH, width=150)
    st.title("Create an account")

    if REGISTER_URL.strip():
        st.markdown(f"[Open the registration page]({REGISTER_URL.strip()})")
    else:
        st.info(
            "The registration page is not connected yet. "
            "Add the link in frontend/config.py to switch it on."
        )

    st.write("")
    if st.button("Back to Sign In"):
        st.session_state["page"] = "login"
        st.rerun()
