import streamlit as st
from Register import register
from login import login
from Dashboard import dashboard


if "page" not in st.session_state:
    st.session_state.page = "login"



if st.session_state.page == "register":

    register()

elif st.session_state.page == "login":

    login()

elif st.session_state.page == "dashboard":

    dashboard()