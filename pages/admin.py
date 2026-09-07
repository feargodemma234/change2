import streamlit as st
from utils.ui import inject_css

st.set_page_config(page_title="Admin - Change2", layout="wide")
inject_css()

st.markdown('<span class="section-label">CHANGE2.COM</span>', unsafe_allow_html=True)
st.markdown('<h1>Admin Dashboard</h1>', unsafe_allow_html=True)

st.metric("Total Orders", "24")
st.metric("Total Revenue", "₦1,250,000")

st.info("This is admin only. Add product management here later.")

st.write("© 2026 Change2")