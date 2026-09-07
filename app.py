import streamlit as st

from utils.auth import get_current_user, logout
from utils.cart import cart_count, init_cart, add_to_cart
from utils.database import get_products
from utils.ui import inject_css, money


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Change2 — Shop. Pay. Delivered.",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# INITIALIZE
# ---------------------------------------------------------

inject_css()
init_cart()

if "user" not in st.session_state:
    st.session_state.user = get_current_user()

user = st.session_state.get("user")


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------

col1, col2, col3 = st.columns([2.5, 5, 2.5])

with col1:
    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">C2</span>
            <span>Change2</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    nav1, nav2, nav3, nav4 = st.columns(4)

    with nav1:
        if st.button("Home", use_container_width=True):
            st.switch_page("app.py")

    with nav2:
        if st.button("Shop", use_container_width=True):
            st.switch_page("pages/products.py")

    with nav3:
        if st.button("Cart", use_container_width=True):
            st.switch_page("pages/cart.py")

    with nav4:
        if st.button("Orders", use_container_width=True):
            if user:
                st.switch_page("pages/orders.py")
            else:
                st.switch_page("pages/login.py")

with col3:
    account1, account2 = st.columns(2)

    with account1:
        if user:
            if st.button("Account", use_container_width=True):
                st.switch_page("pages/account.py")
        else:
            if st.button("Login", use_container_width=True):
                st.switch_page("pages/login.py")

    with account2:
        count = cart_count()

        if st.button(f"🛒 {count}", use_container_width=True):
            st.switch_page("pages/cart.py")


st.markdown("---")


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

hero_left, hero_right = st.columns([1.15, 0.85], gap="large")

with hero_left:

    st.markdown(
        """
        <div class="hero-section">

            <div class="hero-badge">
                ✦ THE NEW WAY TO SHOP
            </div>

            <h1 class="hero-title">
                Global shopping.<br>
                <span>Built for speed.</span>
            </h1>

            <p class="hero-text">
                Discover products, add them to your cart,
                checkout securely and get your order delivered.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    button1, button2 = st.columns(2)

    with button1:
        if st.button(
            "🛍️ Start Shopping",
            type="primary",
            use_container_width=True,
        ):
            st.switch_page("pages/products.py")

    with button2:
        if st.button(
            "View Cart",
            use_container_width=True,
        ):
            st.switch_page("pages/cart.py")


with hero_right:

    # Use a real image URL here.
    # Replace this URL with your own Change2 image later.

    hero_image = (
        "https://images.unsplash.com/"
        "photo-1556742049-0cfed4f6a45d"
        "?auto=format&fit=crop&w=1200&q=85"
    )

    st.image(
        hero_image,
        use_container_width=True,
    )


# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------

st.markdown(
    """
    <div class="section-heading">
        <h2>Everything you need to shop</h2>
        <p>A simple shopping experience from product discovery to delivery.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🛍️</div>
            <h3>Shop</h3>
            <p>Browse products and discover something you love.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🛒</div>
            <h3>Cart</h3>
            <p>Add products and automatically calculate your total.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💳</div>
            <h3>Payment</h3>
            <p>Choose from the payment methods available in the store.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with f4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📦</div>
            <h3>Delivery</h3>
            <p>Track your order from checkout to delivery.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# FEATURED PRODUCTS
# ---------------------------------------------------------

st.markdown(
    """
    <div class="section-heading">
        <h2>Featured products</h2>
        <p>Explore some of the products available on Change2.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    products = get_products(limit=8)
except Exception:
    products = []


if products:

    for row_start in range(0, len(products), 4):

        row = products[row_start:row_start + 4]

        cols = st.columns(4, gap="medium")

        for col, product in zip(cols, row):

            with col:

                image_url = product.get("image_url", "")
                name = product.get("name", "Product")
                description = product.get("description", "")
                category = product.get("category", "General")
                price = float(product.get("price", 0))
                stock = int(product.get("stock", 0))
                product_id = product.get("id")

                if image_url:
                    st.image(
                        image_url,
                        use_container_width=True,
                    )
                else:
                    st.markdown(
                        """
                        <div class="product-placeholder">
                            🛍️
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
                    <div class="product-info">
                        <div class="product-category">
                            {category}
                        </div>

                        <h3>{name}</h3>

                        <p>{description[:100]}</p>

                        <div class="product-price">
                            {money(price)}
                        </div>

                        <div class="product-stock">
                            {stock} available
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if stock > 0:

                    if st.button(
                        "Add to cart",
                        key=f"home_add_{product_id}",
                        use_container_width=True,
                    ):

                        success, message = add_to_cart(
                            product_id,
                            1,
                        )

                        if success:
                            st.success(message)
                        else:
                            st.error(message)

                else:

                    st.button(
                        "Out of stock",
                        key=f"home_out_{product_id}",
                        disabled=True,
                        use_container_width=True,
                    )

else:

    st.info(
        "No products are available yet. "
        "Add products from the administrator dashboard."
    )


# ---------------------------------------------------------
# SHOP CTA
# ---------------------------------------------------------

st.markdown(
    """
    <div class="cta-section">

        <div>
            <div class="hero-badge">
                CHANGE2
            </div>

            <h2>
                Ready to find your next product?
            </h2>

            <p>
                Browse the full Change2 catalog and start shopping.
            </p>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

if st.button(
    "Explore all products →",
   type="primary",
    use_container_width=True,
):
    st.switch_page("pages/products.py")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">

        <div class="footer-brand">
            <strong>Change2</strong>
        </div>

        <p>
            Shop. Pay. Delivered.
        </p>

        <div class="footer-links">
            <span>Products</span>
            <span>Orders</span>
            <span>Payments</span>
            <span>Delivery</span>
        </div>

        <div class="footer-bottom">
            © 2026 Change2. All rights reserved.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)