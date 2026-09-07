import streamlit as st
from utils.ui import inject_css, money
from utils.cart import cart_count, add_to_cart
from utils.database import get_products

st.set_page_config(page_title="Products - Change2", page_icon="🛍️", layout="wide")
inject_css()

# HEADER
st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>Products</h1>', unsafe_allow_html=True)

# SEARCH + CART
col1, col2 = st.columns([4, 1])
with col1:
    search = st.text_input("Search", placeholder="Search for a product...", label_visibility="collapsed")
with col2:
    st.button(f"🛒 Cart ({cart_count()})")

# CATEGORY FILTER
category = st.selectbox("Filter", ["All", "Electronics", "Fashion", "Delivery"])

st.divider()

# GET PRODUCTS
products = get_products()

if not products:
    # EMPTY STATE - FIXED
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/6134/6134065.png", width=120)
        st.markdown("<h3 style='text-align:center'>No products found</h3>", unsafe_allow_html=True)
        st.write("Try a different search or check back later")
else:
    # PRODUCT GRID
    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i % 3]:
            st.image(product.get("image", "https://via.placeholder.com/300"), use_container_width=True)
            st.markdown(f"<h4>{product['name']}</h4>", unsafe_allow_html=True)
            st.write(money(product['price']))
            if st.button("Add to Cart", key=product['id']):
                add_to_cart(product)
                st.rerun()

st.divider()
st.write("© 2026 Change2")