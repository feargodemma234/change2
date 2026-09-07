import streamlit as st
from utils.ui import inject_css, money
from utils.cart import cart_total, clear_cart

st.set_page_config(page_title="Checkout - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>Checkout</h1>', unsafe_allow_html=True)

st.write(f"**Total:** {money(cart_total())}")
st.text_input("Delivery Address")
st.selectbox("Payment Method", ["Pay on Delivery", "Card"])

if st.button("Place Order", type="primary"):
    clear_cart()
    st.switch_page("pages/order_success.py?order_id=ORD003")

st.write("© 2026 Change2")