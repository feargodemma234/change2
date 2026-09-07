import streamlit as st
from utils.ui import inject_css, money
from utils.database import get_orders

st.set_page_config(page_title="Orders - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>My Orders</h1>', unsafe_allow_html=True)
st.divider()

orders = get_orders()

if not orders:
    st.info("You have no orders yet")
else:
    for order in orders:
        with st.container():
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.write(f"**Order:** {order['id']}")
                st.write(f"Date: {order['date']}")
            with col2:
                st.write(f"Total: {money(order['total'])}")
                st.write(f"Items: {order['items']}")
            with col3:
                st.success(order['status'])
        st.divider()

st.write("© 2026 Change2")