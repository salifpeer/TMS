import streamlit as st
from datetime import date

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Employee Registration",
    page_icon="👤",
    layout="wide"
)

# =========================================================
# PAGE HEADER
# =========================================================

st.title("Employee Registration")

st.caption(
    "Please enter your details to create your employee profile."
)

# =========================================================
# REGISTRATION FORM
# =========================================================

with st.form("employee_registration_form"):

    # =====================================================
    # 1. PERSONAL DETAILS
    # =====================================================

    st.subheader("1. Personal Details")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

        with col2:

            email = st.text_input(
                "Email",
                placeholder="example@email.com"
            )

        col1, col2 = st.columns(2)

        with col1:

            date_of_birth = st.date_input(
                "Date of Birth",
                value=date(2000, 1, 1),
                min_value=date(1950, 1, 1),
                max_value=date.today()
            )

        with col2:

            gender = st.selectbox(
                "Gender",
                [
                    "Select",
                    "Female",
                    "Male",
                    "Other"
                ]
            )

        col1, col2 = st.columns(2)

        with col1:

            marital_status = st.selectbox(
                "Marital Status",
                [
                    "Select",
                    "Single",
                    "Married"
                ]
            )

        with col2:

            nationality = st.text_input(
                "Nationality",
                value="Indian"
            )


    # =====================================================
    # 2. CONTACT & ADDRESS DETAILS
    # =====================================================

    st.subheader("2. Contact & Address Details")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            mobile = st.text_input(
                "Mobile Number",
                placeholder="Enter 10-digit mobile number"
            )

        with col2:

            alternate_mobile = st.text_input(
                "Alternate Mobile Number",
                placeholder="Enter 10-digit mobile number"
            )

        st.write("Present Address")

        present_address = st.text_area(
            "Present Address",
            placeholder="Enter your complete address",
            label_visibility="collapsed"
        )


    # =====================================================
    # SUBMIT BUTTON
    # =====================================================

    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        submit = st.form_submit_button(
            "Submit Registration",
            width="stretch",
            type="primary"
        )

# =========================================================
# Form Validation
# =========================================================

if submit:

    # Check if any required field is missing
    if (
        not full_name.strip()
        or not email.strip()
        or gender == "Select"
        or marital_status == "Select"
        or not nationality.strip()
        or not mobile.strip()
        or not alternate_mobile.strip()
        or not present_address.strip()
    ):
        st.error("Please fill all the fields.")

    # Email validation
    elif (
        "@" not in email
        or "." not in email
        or email.startswith("@")
        or email.endswith("@")
    ):
        st.error("Please enter a valid email address.")

    # Mobile number validation
    elif not mobile.isdigit() or len(mobile) != 10:
        st.error("Mobile number must contain exactly 10 digits.")

    # Alternate mobile validation
    elif (
        not alternate_mobile.isdigit()
        or len(alternate_mobile) != 10
    ):
        st.error(
            "Alternate mobile number must contain exactly 10 digits."
        )

    # Everything is valid
    else:
        st.success(
            "Registration submitted successfully!"
        )