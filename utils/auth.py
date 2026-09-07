import streamlit as st
from supabase import create_client, Client


# =========================================================
# SUPABASE CLIENT
# =========================================================

@st.cache_resource
def get_supabase() -> Client:
    """
    Creates and caches the Supabase client.
    Credentials are loaded from Streamlit secrets.
    """

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]

    return create_client(url, key)


# =========================================================
# SESSION INITIALIZATION
# =========================================================

def init_auth():
    """
    Initializes authentication-related session variables.
    """

    if "user" not in st.session_state:
        st.session_state.user = None

    if "session" not in st.session_state:
        st.session_state.session = None


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user():
    """
    Returns the currently logged-in Supabase user.

    Returns:
        User object or None
    """

    init_auth()

    # Already stored in Streamlit session
    if st.session_state.user is not None:
        return st.session_state.user

    try:

        supabase = get_supabase()

        response = supabase.auth.get_user()

        if response and response.user:

            st.session_state.user = response.user

            return response.user

    except Exception:
        pass

    return None


# =========================================================
# SIGN UP
# =========================================================

def signup_user(
    email: str,
    password: str,
    full_name: str,
):
    """
    Creates a new Supabase account.

    Email confirmation is controlled by Supabase settings.
    """

    email = email.strip().lower()
    full_name = full_name.strip()

    if not email:
        return False, "Please enter your email address."

    if not password:
        return False, "Please enter a password."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not full_name:
        return False, "Please enter your full name."

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            }
        )

        if response.user:

            # If Supabase requires email confirmation,
            # session can be None until confirmation.
            if response.session:

                st.session_state.user = response.user
                st.session_state.session = response.session

                return True, "Account created successfully."

            return True, (
                "Account created. "
                "Please check your email and confirm your account "
                "before logging in."
            )

        return False, "Unable to create your account."

    except Exception as e:

        message = str(e)

        if "already registered" in message.lower():
            return False, "An account with this email already exists."

        if "password" in message.lower():
            return False, "Please choose a stronger password."

        return False, "Unable to create your account. Please try again."


# =========================================================
# LOGIN
# =========================================================

def login_user(
    email: str,
    password: str,
):
    """
    Logs a user into Supabase.
    """

    email = email.strip().lower()

    if not email:
        return False, "Please enter your email address."

    if not password:
        return False, "Please enter your password."

    try:

        supabase = get_supabase()

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        if response.user and response.session:

            st.session_state.user = response.user
            st.session_state.session = response.session

            return True, "Login successful."

        return False, "Invalid login details."

    except Exception as e:

        message = str(e).lower()

        if "email not confirmed" in message:
            return False, (
                "Please confirm your email address "
                "before logging in."
            )

        if "invalid login credentials" in message:
            return False, "Incorrect email or password."

        return False, "Login failed. Please try again."


# =========================================================
# LOGOUT
# =========================================================

def logout():
    """
    Logs the current user out of Supabase.
    """

    try:

        supabase = get_supabase()

        supabase.auth.sign_out()

    except Exception:
        pass

    # Clear authentication session
    st.session_state.user = None
    st.session_state.session = None


# =========================================================
# REQUIRE LOGIN
# =========================================================

def require_login():
    """
    Stops access to a page if the customer is not logged in.

    Returns:
        User object when authenticated.
        None otherwise.
    """

    user = get_current_user()

    if user is None:

        st.warning(
            "You need to log in to access this page."
        )

        if st.button(
            "Go to Login",
            type="primary",
            use_container_width=True,
        ):
            st.switch_page("pages/login.py")

        st.stop()

    return user


# =========================================================
# GET USER ID
# =========================================================

def get_user_id():
    """
    Returns the authenticated user's UUID.
    """

    user = get_current_user()

    if user is None:
        return None

    return str(user.id)


# =========================================================
# GET USER EMAIL
# =========================================================

def get_user_email():
    """
    Returns the authenticated user's email.
    """

    user = get_current_user()

    if user is None:
        return None

    return user.email


# =========================================================
# ADMIN CHECK
# =========================================================

def is_admin():
    """
    Checks whether the current authenticated user
    has the administrator role.

    The final authorization is also enforced by Supabase
    Row Level Security. This function is only the UI-level check.
    """

    user = get_current_user()

    if user is None:
        return False

    try:

        supabase = get_supabase()

        response = (
            supabase
            .table("profiles")
            .select("role")
            .eq("id", str(user.id))
            .single()
            .execute()
        )

        if response.data:

            return response.data.get("role") == "admin"

    except Exception:
        return False

    return False


# =========================================================
# REQUIRE ADMIN
# =========================================================

def require_admin():
    """
    Protects administrator pages.

    The database must still enforce administrator
    permissions using RLS.
    """

    user = require_login()

    if not is_admin():

        st.error(
            "You do not have permission to access "
            "the administrator dashboard."
        )

        st.stop()

    return user