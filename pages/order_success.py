import streamlit as st
from utils.ui import inject_css, money
from utils.database import get_order
from utils.cart import clear_cart

st.set_page_config(page_title="Order Success - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>🎉 Order Placed!</h1>', unsafe_allow_html=True)

order_id = st.query_params.get("order_id", "ORD001")
order = get_order(order_id)

if order:
    st.success(f"Your order {order['id']} was placed successfully")
    st.write(f"**Total:** {money(order['total'])}")
    st.write(f"**Status:** {order['status']}")
    st.write(f"**Date:** {order['date']}")
    clear_cart()
else:
    st.info("Order details not found")

if st.button("Continue Shopping"):
    st.switch_page("pages/products.py")

st.write("© 2026 Change2")