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

        # ---------------------------------------------
        # Profile photo + basic information
        # ---------------------------------------------

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
                    "Full Name *",
                    placeholder="Enter your full name"
                )

            with col2:

                email = st.text_input(
                    "Email *",
                    placeholder="example@email.com"
                )

            col1, col2 = st.columns(2)

            with col1:

                date_of_birth = st.date_input(
                    "Date of Birth *",
                    value=date(2000, 1, 1),
                    min_value=date(1950, 1, 1),
                    max_value=date.today()
                )

            with col2:

                gender = st.selectbox(
                    "Gender *",
                    [
                        "Select",
                        "Female",
                        "Male",
                        "Other",
                    
                    ]
                )

            col1, col2 = st.columns(2)

            with col1:

                marital_status = st.selectbox(
                    "Marital Status",
                    [
                        "Select",
                        "Single",
                        "Married",
                    
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

        # ---------------------------------------------
        # Contact
        # ---------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            mobile = st.text_input(
                "Mobile Number *",
                placeholder="Enter 10-digit mobile number"
            )

        with col2:

            alternate_mobile = st.text_input(
                "Alternate Mobile Number",
                placeholder="Enter alternate number"
            )


        # ---------------------------------------------
        # Present Address
        # ---------------------------------------------

        st.write("Present Address")

        present_address = st.text_area(
            "Present Address",
            placeholder="Enter your complete address",
           
        )

       


    # =====================================================
    # 3. EDUCATIONAL DETAILS
    # =====================================================

    st.subheader("3. Educational Details")

    with st.container(border=True):

        # ---------------------------------------------
        # Highest qualification
        # ---------------------------------------------

        highest_qualification = st.selectbox(
            "Highest Qualification *",
            [
                "Select",
                "10th",
                "12th",
                "Bachelor's Degree",
                "Master's Degree",
                
            ]
        )


        # ---------------------------------------------
        # School details
        # ---------------------------------------------

        col1, col2, = st.columns(2)

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


        # ---------------------------------------------
        # Higher education
        # ---------------------------------------------

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
# FORM SUBMISSION
# =========================================================

if submit:

    errors = []


    # ---------------------------------------------
    # Basic validation
    # ---------------------------------------------

    if not full_name.strip():

        errors.append(
            "Full Name is required."
        )


    if not email.strip():

        errors.append(
            "Email is required."
        )


    if not mobile.strip():

        errors.append(
            "Mobile Number is required."
        )


    if gender == "Select":

        errors.append(
            "Please select Gender."
        )


    if highest_qualification == "Select":

        errors.append(
            "Please select Highest Qualification."
        )


    if not photo:

        errors.append(
            "Please upload a profile photo."
        )



        # -----------------------------------------
        # Data structure
        # -----------------------------------------

        employee_data = {

            "personal_details": {

                "full_name": full_name,

                "email": email,

                "date_of_birth": str(
                    date_of_birth
                ),

                "gender": gender,

                "marital_status": marital_status,

                "nationality": nationality
            },


            "contact_address": {

                "mobile": mobile,

                "alternate_mobile": alternate_mobile,

                "present_address": present_address,

                "present_city": present_city,

                "present_state": present_state,

                "present_pincode": present_pincode,

                "permanent_address": permanent_address,

                "permanent_city": permanent_city,

                "permanent_state": permanent_state,

                "permanent_pincode": permanent_pincode
            },


            "education": {

                "highest_qualification":
                    highest_qualification,

                "tenth_percentage":
                    tenth_percentage,

                "twelfth_percentage":
                    twelfth_percentage,

                "twelfth_stream":
                    twelfth_stream,

                "degree":
                    degree,

                "specialization":
                    specialization,

                "university":
                    university,

                "passing_year":
                    passing_year,

                "graduation_percentage":
                    graduation_percentage
            }
        }


        # -----------------------------------------
        # Success message
        # -----------------------------------------

        st.success(
            "Registration completed successfully!"
        )


        # -----------------------------------------
        # Temporary preview
        #
        # Later this will be replaced with
        # requests.post() to FastAPI.
        # -----------------------------------------

        with st.expander(
            "Preview Submitted Data"
        ):

            st.json(employee_data)


        # -----------------------------------------
        # Show uploaded photo
        # -----------------------------------------

        if photo:

            st.write("Profile Photo")

            st.image(
                photo,
                width=150
            )