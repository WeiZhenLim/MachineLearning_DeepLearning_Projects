import streamlit as st

# Load utils
from utils import show_banner

def home_page():
    show_banner()
    st.title("Home 🏠")

    st.subheader("Early Stage Diabetes Risk Predictor App")
    st.write("""
             This app predicts the risk of developing early-stage diabetes using ML models trained on a dataset
             containing signs and symptoms of newly diagnosed or at-risk diabetic patients.
             """)

    st.subheader("Data Source")
    st.write("Early Stage Diabetes Risk Prediction Dataset from UCI Machine Learning Repository")
    st.write("🔗[**Link to Data Source**](https://archive.ics.uci.edu/dataset/529/early+stage+diabetes+risk+prediction+dataset)")

    st.subheader("App Content")
    st.write("This app contains multiple sections to guide users through the diabetes prediction process:")
    st.write("1️⃣ **Home:** Provides an overview of the application and its purpose.")
    st.write("2️⃣ **Exploratory Data Analysis (EDA):** Visualizes and explores key trends in the dataset.")
    st.write("3️⃣ **Diabetes Prediction (ML):** Uses machine learning models to predict diabetes risk based on input data.")
    st.write("4️⃣ **About:** Offers information about the dataset, methodology, and application development.")

def about_page():
    show_banner()
    st.title("About Page 📖")