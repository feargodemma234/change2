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
    st.markdown('<div class="brand">CHANGE2</div>', unsafe_allow_html=True) # FIXED

with col2:
    st.text_input("Search", placeholder="Search products, delivery...", label_visibility="collapsed", key="search")

with col3:
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.button(f"🛒 {cart_count()}")
    with c2: 
        st.button("📦 Orders")
    with c3: 
        if user: 
            st.button("Logout", on_click=logout)
        else: 
            st.button("Login")

st.divider()

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>Shop. Pay. Delivered.</h1>', unsafe_allow_html=True)

st.image(
    "https://images.unsplash.com/photo-1586528113085-9100e3e2b122?q=80&w=1200&auto=format&fit=crop", 
    use_container_width=True,
    caption="Fast Delivery Across Nigeria"
)

st.write("Get anything delivered from Onitsha to anywhere in Nigeria. Pay with Naira or BTC.")

# ---------------------------------------------------------
# CTA BUTTON
# ---------------------------------------------------------

if st.button(  # FIXED: was missing st.button
    "Browse Products",
    type="primary",
    use_container_width=True,
):
    st.switch_page("pages/products.py")

st.divider()

# ---------------------------------------------------------
# MY ORDERS SECTION
# ---------------------------------------------------------

st.markdown('<span class="section-label">MY ACCOUNT</span>', unsafe_allow_html=True)
st.markdown('<h2>My Orders</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/4076/4076503.png", width=120) # Box icon
    st.subheader("No orders yet")
    st.write("Your completed purchases will appear here")

st.divider()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .footer {text-align: center; padding: 40px 20px; background: #0f172a; color: #cbd5e1; margin-top: 50px; border-radius: 12px;}
    .footer-brand {font-size: 20px; margin-bottom: 8px; color: white;}
    .footer-links span {margin: 0 12px; cursor: pointer; color: #94a3b8;}
    .footer-links span:hover {color: white;}
    .footer-bottom {margin-top: 20px; font-size: 12px; color: #94a3b8;}
    .brand {font-size: 24px; font-weight: 800; color: #0f172a;}
    .section-label {color: #64748b; font-size: 12px; letter-spacing: 1px;}
    </style>

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
    unsafe_allow_html=True, # FIXED: this makes HTML render
)