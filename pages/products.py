import streamlit as st
from utils.ui import inject_css, money
from utils.cart import cart_count, add_to_cart
from utils.database import get_products

st.set_page_config(page_title="Products - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>Products</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    search = st.text_input("Search", placeholder="Search for a product...", label_visibility="collapsed")
with col2:
    if st.button(f"🛒 Cart ({cart_count()})"):
        st.switch_page("pages/cart.py")

category = st.selectbox("Filter", ["All", "Electronics", "Fashion", "Delivery"])
st.divider()

products = get_products()
if category != "All":
    products = [p for p in products if p['category'] == category]

cols = st.columns(3)
for i, product in enumerate(products):
    with cols[i % 3]:
        st.image(product['image'], use_container_width=True)
        st.markdown(f"<h4>{product['name']}</h4>", unsafe_allow_html=True)
        st.write(money(product['price']))
        if st.button("Add to Cart", key=product['id']):
            add_to_cart(product)
            st.rerun()

st.divider()
st.write("© 2026 Change2")