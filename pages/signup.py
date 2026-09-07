import streamlit as st

from utils.auth import signup_user
from utils.ui import inject_css
from utils.security import valid_email

st.set_page_config(
    page_title="Create Account | Change2.com",
    page_icon="👤",
    layout="wide",
)

inject_css()

st.markdown(
    """
    <div class="form-card">
        <div class="form-title">Create your account</div>
        <div class="form-subtitle">
            Join Change2.com and start shopping.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

full_name = st.text_input(
    "Full name",
    placeholder="Your full name",
)

email = st.text_input(
    "Email address",
    placeholder="you@example.com",
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="At least 8 characters",
)

confirm_password = st.text_input(
    "Confirm password",
    type="password",
    placeholder="Enter your password again",
)

if st.button(
    "Create Account",
    type="primary",
    use_container_width=True,
):

    if not full_name.strip():
        st.error("Please enter your full name.")

    elif not valid_email(email):
        st.error("Please enter a valid email address.")

    elif len(password) < 8:
        st.error("Password must contain at least 8 characters.")

    elif password != confirm_password:
        st.error("The passwords do not match.")

    else:

        success, message = signup_user(
            email,
            password,
            full_name,
        )

        if success:
            st.success(message)

            if st.session_state.get("user"):
                st.switch_page("app.py")
            else:
                st.info(
                    "Check your email to confirm your account, "
                    "then log in."
                )

        else:
            st.error(message)

st.write("")

if st.button(
    "Already have an account? Login",
    use_container_width=True,
):
    st.switch_page("pages/login.py")

if st.button(
    "← Back to Home",
    use_container_width=True,
):
    st.switch_page("app.py")