import streamlit as st

tab1,tab2,tab3=st.tabs(["My Dashboard","Details","Leaves"])
with st.sidebar:
    c1,c2=st.columns([5,3])
    with c1:
        st.write(" ")
    with c2:
     st.sidebar.title("My dashboard")
     st.sidebar.image("https://th.bing.com/th/id/OIP.G37tgeQqSNt7v2oPfj9ltQHaE7?w=205&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",width=100)
     st.sidebar.write("name")
     st.sidebar.write("id")
     st.sidebar.write("email")
     st.sidebar.button("Sign out",type="primary")







col1,con,col2=st.columns([3,3,3])



with col1:
    st.button("Apply Leave",width=100,type="primary")
with con:
     st.button("Check in",type="primary",width=100)
with col2:
    st.button("Apply WFH",width=100,type="primary")



st.subheader("Check-in and check-out Details Report")



cont1=st.container(border=True)
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




    col1, col2, col3, col4, col5, col6, col7 = st.columns(
        [2, 2, 2, 2, 1.5, 2.5, 2.5]
    )

    with col1:
        st.button(
            "Check Out",
            key="checkout_1",
            use_container_width=True
        )

    with col2:
        st.button(
            "Take Break",
            key="break_1",
            use_container_width=True
        )

    with col3:
        st.button(
            "Resume",
            key="resume_1",
            use_container_width=True
        )

    with col4:
        st.write("CBXNS381 - Salif Peer")

    with col5:
        st.write("Checked In")

    with col6:
        st.write("24-Sep-2026 09:48 AM")

    with col7:
        st.write("-")




    col1, col2, col3, col4, col5, col6, col7 = st.columns(
        [2, 2, 2, 2, 1.5, 2.5, 2.5]
    )

    with col1:
        st.button(
            "Check Out",
            key="checkout_2",
            use_container_width=True
        )

    with col2:
        st.button(
            "Take Break",
            key="break_2",
            use_container_width=True
        )

    with col3:
        st.button(
            "Resume",
            key="resume_2",
            use_container_width=True
        )

    with col4:
        st.write("CBXNS381 - Salif Peer")

    with col5:
        st.write("Checked Out")

    with col6:
        st.write("23-Sep-2026 09:55 AM")

    with col7:
        st.write("06:00 PM")