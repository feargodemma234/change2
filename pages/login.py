import streamlit as st

from utils.auth import login_user
from utils.ui import inject_css

st.set_page_config(
    page_title="Login | Change2.com",
    page_icon="🔐",
    layout="wide",
)

inject_css()

st.markdown(
    """
    <div class="form-card">
        <div class="form-title">Welcome back</div>
        <div class="form-subtitle">
            Log in to your Change2.com account.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

email = st.text_input(
    "Email address",
    placeholder="you@example.com",
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Your password",
)

if st.button(
    "Login",
    type="primary",
    use_container_width=True,
):

    success, message = login_user(
        email,
        password,
    )

    if success:
        st.success(message)
        st.session_state.user = st.session_state.get("user")
        st.switch_page("app.py")
    else:
        st.error(message)

st.write("")

if st.button(
    "Create a new account",
    use_container_width=True,
):
    st.switch_page("pages/signup.py")

if st.button(
    "← Back to Home",
    use_container_width=True,
):
    st.switch_page("app.py")