import streamlit as st
from utils.ui import inject_css, money
from utils.cart import get_cart, remove_from_cart, cart_total

st.set_page_config(page_title="Cart - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>Your Cart</h1>', unsafe_allow_html=True)
st.divider()

cart = get_cart()

if not cart:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/263/263142.png", width=120)
        st.markdown("<h3 style='text-align:center'>Your cart is empty</h3>", unsafe_allow_html=True)
        if st.button("Continue Shopping", use_container_width=True):
            st.switch_page("pages/products.py")
else:
    for item in cart:
        col1, col2, col3 = st.columns([1,3,1])
        with col1: st.image(item['image'], width=80)
        with col2: 
            st.write(f"**{item['name']}**")
            st.write(f"Qty: {item['qty']} | {money(item['price'])}")
        with col3: 
            if st.button("Remove", key=f"del_{item['id']}"):
                remove_from_cart(item['id'])
                st.rerun()
        st.divider()
    
    st.markdown(f"<h2 style='text-align:right'>Total: {money(cart_total())}</h2>", unsafe_allow_html=True)
    if st.button("Checkout", type="primary", use_container_width=True):
        st.switch_page("pages/order_success.py?order_id=ORD001")

st.write("© 2026 Change2")