import streamlit as st
from utils.ui import inject_css

st.set_page_config(page_title="Home - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1 class="brand">Welcome to Change2</h1>', unsafe_allow_html=True)
st.write("Shop. Pay. Delivered.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Browse Products", use_container_width=True):
        st.switch_page("pages/products.py")
with col2:
    if st.button("My Orders", use_container_width=True):
        st.switch_page("pages/orders.py")
with col3:
    if st.button("Cart", use_container_width=True):
        st.switch_page("pages/cart.py")

st.divider()
st.write("© 2026 Change2")