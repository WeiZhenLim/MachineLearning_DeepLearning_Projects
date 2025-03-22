import streamlit as st

def show_banner():
    st.markdown("""
        <style>
            .banner {
                background: linear-gradient(to bottom, #5B86E5, #36D1DC);
                padding: 10px;
                text-align: center;
                border-radius: 10px;
                color: white;
            }
        </style>
        <div class="banner">
            <h1>💬 Twitter Tweets Sentiment Analysis App</h1>
            <p>Analyzing tweet sentiments using Natural Language Processing and ML models</p>
        </div>
    """, unsafe_allow_html=True)

def expander_formatter(fontsize):
    st.markdown(
    f"""
    <style>
    div[data-testid="stExpander"] :not(div[data-testid="stExpanderDetails"] *)  {{
    font-size: {fontsize}px;
    font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True)