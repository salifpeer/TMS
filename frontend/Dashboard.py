import streamlit as st
import requests


URL = "http://127.0.0.1:8000"


if "attendance" not in st.session_state:

    st.session_state.attendance = {
        "status": "-",
        "checkin_time": "-",
        "checkout_time": "-"
    }



def checkin():

    employee_id = st.session_state.employee_id

    response = requests.post(
        f"{URL}/checkin",
        params={
            "employee_id": employee_id
        }
    )

    data = response.json()

    
    st.session_state.attendance = data

    st.toast(
        data["message"],
        icon="✅"
    )




def checkout():

    employee_id = st.session_state.employee_id

    response = requests.post(
        f"{URL}/checkout",
        params={
            "employee_id": employee_id
        }
    )

    data = response.json()


    st.session_state.attendance = data

    st.toast(
        data["message"],
        icon="✅"
    )




def take_break():

    employee_id = st.session_state.employee_id

    response = requests.post(
        f"{URL}/break/start",
        params={
            "employee_id": employee_id
        }
    )

    data = response.json()

    
    st.session_state.attendance = data

    st.toast(
        data["message"],
        icon="☕"
    )




def resume_break():

    employee_id = st.session_state.employee_id

    response = requests.post(
        f"{URL}/break/resume",
        params={
            "employee_id": employee_id
        }
    )

    data = response.json()


    st.session_state.attendance = data

    st.toast(
        data["message"],
        icon="▶️"
    )




tab1, tab2, tab3 = st.tabs(
    ["My Dashboard", "Details", "Leaves"]
)




with st.sidebar:

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:

        st.title("My Dashboard")

        st.image(
            "https://th.bing.com/th/id/OIP.G37tgeQqSNt7v2oPfj9ltQHaE7?w=205&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&pid=1.7&rm=3",
            width=100
        )

        st.write("Name")
        st.write("ID")
        st.write("Email")

        st.button(
            "Sign out",
            type="primary"
        )


col1, con, col2 = st.columns([3, 3, 3])


with col1:

    st.button(
        "Apply Leave",
        width=100,
        type="primary"
    )


with con:

    st.button(
        "Check In",
        type="primary",
        width=100,
        on_click=checkin
    )


with col2:

    st.button(
        "Apply WFH",
        width=100,
        type="primary"
    )




st.subheader("Check-in and check-out Details Report")


cont1 = st.container(border=True)


with cont1:

    

    col1, col2, col3, col4, col5, col6, col7 = st.columns(
        [2, 2, 2, 2, 1.5, 2.5, 2.5]
    )

    with col1:
        st.write("Check Out")

    with col2:
        st.write("Take Break")

    with col3:
        st.write("Resume Work")

    with col4:
        st.write("Name")

    with col5:
        st.write("Status")

    with col6:
        st.write("Check-In Time")

    with col7:
        st.write("Check-Out Time")


    # ---------------- DATA ----------------

    col1, col2, col3, col4, col5, col6, col7 = st.columns(
        [2, 2, 2, 2, 1.5, 2.5, 2.5]
    )


    
    with col1:

        st.button(
            "Check Out",
            on_click=checkout,
            key="checkout_button"
        )


    

    with col2:

        st.button(
            "Take Break",
            on_click=take_break,
            key="break_button"
        )


    

    with col3:

        st.button(
            "Resume",
            on_click=resume_break,
            key="resume_button"
        )


    

    with col4:

        st.write("CBXNS381 - Salif Peer")




    with col5:

        st.write(
            st.session_state.attendance["status"]
        )


    

    with col6:

        st.write(
            st.session_state.attendance["checkin_time"]
        )


    

    with col7:

        st.write(
            st.session_state.attendance["checkout_time"]
        )