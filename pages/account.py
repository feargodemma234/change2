import streamlit as st
from utils.ui import inject_css

st.set_page_config(page_title="Account - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>My Account</h1>', unsafe_allow_html=True)

st.text_input("Full Name", "Test User")
st.text_input("Email", "user@change2.com")
st.text_input("Phone", "+234 800 000 0000")

if st.button("Save Changes", type="primary"):
    st.success("Account updated!")

st.write("© 2026 Change2")