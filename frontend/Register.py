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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

div[data-testid="stFormSubmitButton"] > button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    padding: 10px 20px;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #45a049;
    color: white;
}

</style>
""", unsafe_allow_html=True)


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

        photo_col, details_col = st.columns([1, 3])

        with photo_col:

            st.write("Profile Photo")

            photo = st.file_uploader(
                "Upload Photo",
                type=["jpg", "jpeg", "png"]
            )

            if photo:
                st.image(
                    photo,
                    width=150
                )

        with details_col:

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
                placeholder="Enter alternate number"
            )

        st.write("Present Address")

        present_address = st.text_area(
            "Present Address",
            placeholder="Enter your complete address",
            label_visibility="collapsed"
        )


    # =====================================================
    # 3. EDUCATIONAL DETAILS
    # =====================================================

    st.subheader("3. Educational Details")

    with st.container(border=True):

        highest_qualification = st.selectbox(
            "Highest Qualification",
            [
                "Select",
                "10th",
                "12th",
                "Bachelor's Degree",
                "Master's Degree"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:

            tenth_percentage = st.number_input(
                "10th Percentage",
                min_value=0.0,
                max_value=100.0,
                step=0.1
            )

        with col2:

            twelfth_percentage = st.number_input(
                "12th Percentage",
                min_value=0.0,
                max_value=100.0,
                step=0.1
            )

        st.write("Higher Education")

        col1, col2 = st.columns(2)

        with col1:

            degree = st.text_input(
                "Degree / Course",
                placeholder="e.g. B.Tech, BCA, M.Tech"
            )

        with col2:

            specialization = st.text_input(
                "Specialization",
                placeholder="e.g. Computer Science, AI/ML"
            )

        col1, col2 = st.columns(2)

        with col1:

            university = st.text_input(
                "University / Institution"
            )

        with col2:

            passing_year = st.number_input(
                "Passing Year",
                min_value=1950,
                max_value=date.today().year + 5,
                value=date.today().year,
                step=1
            )

        col1, col2 = st.columns(2)

        with col1:

            graduation_percentage = st.number_input(
                "Graduation Percentage / CGPA",
                min_value=0.0,
                max_value=100.0,
                step=0.1
            )

        with col2:

            education_document = st.file_uploader(
                "Upload Education Document",
                type=[
                    "pdf",
                    "jpg",
                    "jpeg",
                    "png"
                ]
            )


    # =====================================================
    # SUBMIT BUTTON
    # =====================================================

    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        submit = st.form_submit_button(
            "Submit Registration",
            width="stretch"
        )


# =========================================================
# SIMPLE FRONTEND RESPONSE
# =========================================================

if submit:

    st.success("Registration submitted successfully!")