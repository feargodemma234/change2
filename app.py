import streamlit as st

from utils.auth import get_current_user, logout
from utils.cart import cart_count
from utils.database import get_products
from utils.ui import inject_css, product_card


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Change2.com",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# UI
# ---------------------------------------------------------

inject_css()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "user" not in st.session_state:
    st.session_state.user = get_current_user()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="change2-header">
        <div class="change2-logo">
            <span class="logo-mark">C2</span>
            <span>Change2</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------

user = st.session_state.get("user")

nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(
    [2, 1, 1, 1, 1, 1]
)

with nav1:
    st.markdown(
        """
        <div class="nav-brand">
            Change2.com
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav2:
    if st.button("Home", use_container_width=True):
        st.switch_page("app.py")

with nav3:
    if st.button("Products", use_container_width=True):
        st.switch_page("pages/products.py")

with nav4:
    if st.button(
        f"Cart ({cart_count()})",
        use_container_width=True
    ):
        st.switch_page("pages/cart.py")

with nav5:
    if user:
        if st.button("Account", use_container_width=True):
            st.switch_page("pages/account.py")
    else:
        if st.button("Login", use_container_width=True):
            st.switch_page("pages/login.py")

with nav6:
    if user:
        if st.button("Logout", use_container_width=True):
            logout()
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("Sign up", use_container_width=True):
            st.switch_page("pages/signup.py")


st.markdown("<hr>", unsafe_allow_html=True)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
    <section class="hero">
        <div class="hero-content">
            <div class="hero-badge">
                CHANGE2 MARKETPLACE
            </div>

            <h1>
                Shop smarter.<br>
                <span>Change everything.</span>
            </h1>

            <p>
                Discover products, place orders and track your
                deliveries from one modern marketplace.
            </p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HERO BUTTONS
# ---------------------------------------------------------

hero_left, hero_right = st.columns(2)

with hero_left:
    if st.button(
        "Shop Products →",
        type="primary",
        use_container_width=True
    ):
        st.switch_page("pages/products.py")

with hero_right:
    if st.button(
        "View Cart",
        use_container_width=True
    ):
        st.switch_page("pages/cart.py")


st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# FEATURE CARDS
# ---------------------------------------------------------

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🛒</div>
            <h3>Easy Shopping</h3>
            <p>
                Browse products and add everything you
                need to your cart.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🚚</div>
            <h3>Order Tracking</h3>
            <p>
                Keep track of your orders from payment
                through delivery.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>Secure Accounts</h3>
            <p>
                Your account and order information are
                protected with Supabase authentication.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# PRODUCTS
# ---------------------------------------------------------

st.markdown(
    """
    <div class="section-heading">
        <div>
            <span class="section-label">FEATURED</span>
            <h2>Popular Products</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


products = get_products(limit=8)


if not products:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">📦</div>
            <h3>No products yet</h3>
            <p>
                Products added by the store administrator
                will appear here.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    # Display four products per row
    for start in range(0, len(products), 4):

        row = products[start:start + 4]

        columns = st.columns(4)

        for column, product in zip(columns, row):

            with column:

                product_card(product)

                if st.button(
                    "Add to Cart",
                    key=f"home_add_{product['id']}",
                    use_container_width=True,
                ):

                    product_id = str(product["id"])

                    current_quantity = st.session_state.cart.get(
                        product_id,
                        0
                    )

                    stock = int(product.get("stock", 0))

                    if stock <= 0:

                        st.error("This product is out of stock.")

                    elif current_quantity >= stock:

                        st.warning(
                            "You cannot add more than the available stock."
                        )

                    else:

                        st.session_state.cart[product_id] = (
                            current_quantity + 1
                        )

                        st.success(
                            f"{product['name']} added to cart."
                        )

                        st.rerun()


# ---------------------------------------------------------
# CTA
# ---------------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <section class="cta-section">
        <div>
            <span class="section-label">
                READY TO SHOP?
            </span>

            <h2>
                Find something you'll love.
            </h2>

            <p>
                Explore the complete Change2 product catalog.
            </p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if st.button(
    "Explore All Products →",
    type="primary",
    use_container_width=True,
):
    st.switch_page("pages/products.py")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <footer class="footer">

        <div class="footer-logo">
            Change2.com
        </div>

        <div class="footer-links">
            <span>Shop</span>
            <span>Orders</span>
            <span>Support</span>
            <span>Account</span>
        </div>

        <div class="footer-copy">
            © 2026 Change2.com. All rights reserved.
        </div>

    </footer>
    """,
    unsafe_allow_html=True,
)