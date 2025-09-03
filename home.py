import streamlit as st
from app_pages import page_home, page_misinformation_checker, page2, evidence_context

st.set_page_config(page_title="Evidence App", layout="centered")

def main():
    st.title("Welcome to Sorteria")

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    page = st.sidebar.radio(
        "Go to:", 
        ["Home", "Misinformation Checker", "Fake Profile and Campaign Identification", "Evidence & Contextualization"],
        index=["Home", "Misinformation Checker", "Fake Profile and Campaign Identification", "Evidence & Contextualization"].index(st.session_state.current_page)
    )

    if page != st.session_state.current_page:
        st.session_state.current_page = page
        if page != "Evidence & Contextualization":
            if "form_submitted" in st.session_state:
                del st.session_state.form_submitted
            if "submitted_data" in st.session_state:
                del st.session_state.submitted_data

    if page == "Home":
        page_home.render()
    elif page == "Misinformation Checker":
        page_misinformation_checker.render()
    elif page == "Fake Profile and Campaign Identification":
        page2.render()
    elif page == "Evidence & Contextualization":
        evidence_context.render()

if __name__ == "__main__":
    main()
