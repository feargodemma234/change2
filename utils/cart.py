import streamlit as st

def get_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = []
    return st.session_state.cart

def add_to_cart(product):
    cart = get_cart()
    for item in cart:
        if item['id'] == product['id']:
            item['qty'] += 1
            return
    product['qty'] = 1
    cart.append(product)

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in get_cart() if item['id'] != product_id]

def cart_count():
    return sum(item['qty'] for item in get_cart())

def cart_total():
    return sum(item['price'] * item['qty'] for item in get_cart())