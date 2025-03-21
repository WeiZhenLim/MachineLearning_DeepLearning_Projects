import streamlit as st

def show_banner():
    st.markdown("""
        <style>
            .banner {
                background: linear-gradient(to right, #6a11cb, #2575fc);
                padding: 10px;
                text-align: center;
                border-radius: 10px;
                color: white;
            }
        </style>
        <div class="banner">
            <h1>🔬 Diabetes Prediction App</h1>
            <p>Leveraging ML models to predict diabetes risk</p>
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