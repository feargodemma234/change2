import streamlit as st

from utils.auth import require_login, get_user_email, logout
from utils.database import get_profile, update_profile
from utils.security import clean_text, validate_phone
from utils.ui import inject_css, page_title

st.set_page_config(
    page_title="My Account | Change2.com",
    page_icon="👤",
    layout="wide",
)

inject_css()

user = require_login()
user_id = str(user.id)

page_title(
    "My Account",
    "Manage your Change2.com account.",
)

profile = get_profile(user_id) or {}

left, right = st.columns(2)

with left:

    st.subheader("Personal Information")

    full_name = st.text_input(
        "Full name",
        value=profile.get("full_name", ""),
    )

    phone = st.text_input(
        "Phone number",
        value=profile.get("phone", ""),
    )

    email = st.text_input(
        "Email address",
        value=get_user_email() or "",
        disabled=True,
    )

    if st.button(
        "Save Changes",
        type="primary",
        use_container_width=True,
    ):

        full_name = clean_text(
            full_name,
            150,
        )

        phone = clean_text(
            phone,
            30,
        )

        if not full_name:
            st.error("Please enter your name.")

        elif not validate_phone(phone):
            st.error("Please enter a valid phone number.")

        else:

            success = update_profile(
                user_id,
                full_name,
                phone,
            )

            if success:
                st.success(
                    "Your account has been updated."
                )
            else:
                st.error(
                    "Unable to update your account."
                )


with right:

    st.subheader("Account")

    st.info(
        f"Logged in as:\n\n{get_user_email()}"
    )

    st.write("")

    if st.button(
        "View My Orders",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/orders.py"
        )

    if st.button(
        "Shop Products",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/products.py"
        )

    st.write("")

    if st.button(
        "Log Out",
        use_container_width=True,
    ):

        logout()

        st.session_state.user = None

        st.switch_page(
            "app.py"
        )