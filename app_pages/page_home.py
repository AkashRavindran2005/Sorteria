import streamlit as st

def render():
    st.write("Choose an option below:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Misinformation Checker** \n\nAnalyze claims and detect misinformation")
    with col2:
        st.info("**Fake Profile & Campaign Identification** \n\nDetect impersonation accounts or channels posing as VIPs and identify coordinated misinformation or smear campaigns across Instagram, Twitter, and Facebook.")
    with col3:
        st.info("**Evidence & Contextualization** \n\nReport suspicious content")

    st.markdown("""
    ---
    ### About This App
    This application helps you:
    - **Fact-check claims** using AI-powered analysis
    - **Monitor social media** for misinformation patterns
    - **Track viral content** spread across platforms
    - **Trace origins** of suspicious information
    - **Report evidence** of fake content or accounts
    """)
