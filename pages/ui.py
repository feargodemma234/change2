import streamlit as st

def inject_css():
    st.markdown("""
    <style>
        .brand {font-size: 28px; font-weight: 800; color: #0f172a;}
        .section-label {color: #64748b; font-size: 12px; letter-spacing: 1px;}
        h1, h2, h3, h4 {color: #0f172a;}
    </style>
    """, unsafe_allow_html=True)

def money(n):
    return f"${n:,}"