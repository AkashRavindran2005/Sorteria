import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from backend.fact_checker import FactChecker
from backend.social_monitor import SocialMonitor
from backend.viral_tracker import ViralTracker
from backend.origin_tracer import OriginTracer
import time

st.set_page_config(
    page_title="Rumour Genesis Explorer", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Rumour Genesis Explorer")
st.markdown("**Real-time Fact-checking, Viral Tracking & Origin Tracing**")

@st.cache_resource
def load_components():
    return {
        'fact_checker': FactChecker(),
        'social_monitor': SocialMonitor(),
        'viral_tracker': ViralTracker(),
        'origin_tracer': OriginTracer()
    }

components = load_components()

tab1, tab2, tab3, tab4 = st.tabs(["Fact Check", "Social Monitor", "Viral Analysis", "Origin Trace"])

with tab1:
    st.header("Fact-Check Information")
    
    input_type = st.radio("Input Type:", ["Text", "URL", "Social Media Post"])
    
    if input_type == "Text":
        claim = st.text_area("Enter claim to verify:", height=150)
    elif input_type == "URL":
        claim = st.text_input("Enter URL:")
    else:
        claim = st.text_input("Enter social media post URL/handle:")
    
    if st.button("Check Claim", type="primary"):
        if claim:
            with st.spinner("Analyzing claim..."):
                result = components['fact_checker'].check_fact(claim)
                
            col1, col2 = st.columns([2, 1])
            
            with col1:
                verdict_color = "🟢" if result['verdict'] == "True" else "🔴" if result['verdict'] == "Rumor" else "🟡"
                st.markdown(f"### {verdict_color} Verdict: **{result['verdict']}**")
                st.markdown(f"**Confidence Score:** {result['confidence']:.2%}")
                
                st.markdown("**Evidence & Sources:**")
                for evidence in result['evidence']:
                    st.markdown(f"• {evidence}")
                
                if result.get('similar_claims'):
                    st.markdown("**Similar Claims Found:**")
                    for claim_data in result['similar_claims']:
                        st.markdown(f"• {claim_data}")
            
            with col2:
                fig = go.Figure(data=go.Scatter(
                    x=[0], y=[result['confidence']],
                    mode='markers',
                    marker=dict(size=50, color='red' if result['verdict'] == 'Rumor' else 'green')
                ))
                fig.update_layout(title="Confidence", xaxis_title="", yaxis_title="Score")
                st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Social Media Monitoring")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("VIP Accounts")
        vip_accounts = st.multiselect(
            "Select accounts to monitor:",
            ["@elonmusk", "@Oprah", "@JoeBiden", "@realDonaldTrump", "@BillGates", "@TheRock"],
            default=["@elonmusk", "@Oprah"]
        )
        
        keywords = st.text_input("Keywords to track:", "AI, technology, politics")
        
        if st.button("Start Monitoring"):
            monitoring_data = components['social_monitor'].monitor_accounts(vip_accounts, keywords.split(', '))
            st.session_state.monitoring_data = monitoring_data
    
    with col2:
        st.subheader("Live Feed")
        if 'monitoring_data' in st.session_state:
            for post in st.session_state.monitoring_data:
                st.markdown(f"**@{post['username']}** - {post['platform']}")
                st.markdown(post['content'])
                st.markdown(f"*{post['timestamp']} • {post['engagement']} interactions*")
                st.markdown("---")

with tab3:
    st.header("Viral Content Analysis")
    
    content_url = st.text_input("Enter content URL for viral analysis:")
    
    if st.button("Analyze Virality"):
        if content_url:
            viral_data = components['viral_tracker'].track_viral(content_url)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(
                    viral_data['timeline'], 
                    x='time', y='shares',
                    title="Viral Spread Timeline"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    viral_data['platforms'],
                    x='platform', y='engagement',
                    title="Platform Engagement"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Key Influencers")
            influencer_df = pd.DataFrame(viral_data['influencers'])
            st.dataframe(influencer_df)

with tab4:
    st.header("Origin Tracing")
    
    trace_content = st.text_area("Enter content to trace origin:", height=100)
    
    if st.button("Trace Origin"):
        if trace_content:
            origin_data = components['origin_tracer'].trace_origin(trace_content)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Most Likely Origin:**")
                st.markdown(f"• **Source:** {origin_data['origin']['source']}")
                st.markdown(f"• **Confidence:** {origin_data['origin']['confidence']:.2%}")
                st.markdown(f"• **First Detected:** {origin_data['origin']['timestamp']}")
                
                st.markdown("**Propagation Path:**")
                for hop in origin_data['path']:
                    st.markdown(f"• {hop['platform']} → {hop['username']} ({hop['timestamp']})")
            
            with col2:
                st.markdown("**Network Analysis**")
                network_fig = go.Figure(data=go.Scatter(
                    x=origin_data['network']['x'],
                    y=origin_data['network']['y'],
                    mode='markers+text',
                    text=origin_data['network']['labels'],
                    textposition="middle center"
                ))
                network_fig.update_layout(title="Information Spread Network")
                st.plotly_chart(network_fig, use_container_width=True)

st.sidebar.markdown("### Statistics")
st.sidebar.metric("Claims Checked Today", "1,247")
st.sidebar.metric("Rumors Detected", "89")
st.sidebar.metric("Origins Traced", "156")

st.sidebar.markdown("### Settings")
api_status = st.sidebar.selectbox("API Status", ["Connected", "Disconnected"])
st.sidebar.color_picker("Theme Color", "#FF6B6B")