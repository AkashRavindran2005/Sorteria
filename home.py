import streamlit as st

st.set_page_config(page_title="Home", layout="centered")
st.title("Welcome to the Evidence App")

st.write("Choose an option below:")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/Page1.py", label="Page 1", icon="✨")
with col2:
    st.page_link("pages/Page2.py", label="Page 2", icon="🗂️")
with col3:
    st.page_link(
        "pages/Evidence_and_Contextualization.py",
        label="Evidence & Contextualization", 
        icon="🕵️"
    )
