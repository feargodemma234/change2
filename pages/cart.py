import streamlit as st
from utils.ui import inject_css, money
from utils.cart import get_cart, remove_from_cart, cart_total, cart_count

st.set_page_config(page_title="Cart - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>Your Cart</h1>', unsafe_allow_html=True)
st.divider()

cart = get_cart()

if not cart:
    st.image("https://cdn-icons-png.flaticon.com/512/263/263142.png", width=120)
    st.markdown("<h3>Your cart is empty</h3>", unsafe_allow_html=True)
    st.write("Add some products to your cart")
    if st.button("Continue Shopping"):
        st.switch_page("pages/products.py")
else:
    for item in cart:
        col1, col2, col3 = st.columns([1,3,1])
        with col1: st.image(item['image'], width=80)
        with col2: st.write(f"**{item['name']}** x{item['qty']}")
        with col3: 
            if st.button("X", key=f"del_{item['id']}"):
                remove_from_cart(item['id'])
                st.rerun()
    st.markdown(f"<h2>Total: {money(cart_total())}</h2>", unsafe_allow_html=True)

st.divider()
st.write("© 2026 Change2")