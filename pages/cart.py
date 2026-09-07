import streamlit as st

def init_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = []

def get_cart():
    return st.session_state.get("cart", [])

def add_to_cart(product):
    cart = get_cart()
    # check if already in cart
    for item in cart:
        if item['id'] == product['id']:
            item['qty'] += 1
            return
    product['qty'] = 1
    cart.append(product)
    st.session_state.cart = cart
    st.toast(f"Added {product['name']} to cart")

def remove_from_cart(product_id):
    cart = get_cart()
    st.session_state.cart = [item for item in cart if item['id'] != product_id]

def cart_count():
    return sum(item['qty'] for item in get_cart())

def cart_total():
    return sum(item['price'] * item['qty'] for item in get_cart())