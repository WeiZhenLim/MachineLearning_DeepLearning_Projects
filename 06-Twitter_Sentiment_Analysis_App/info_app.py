import streamlit as st

# Load utils
from utils import show_banner

def home_page():
    show_banner()
    st.title("Home 🏠")

    st.subheader("Twitter Tweets Sentiment Analysis App")
    st.write("""
             This app analyzes the sentiment of tweets using machine learning models trained on labeled Twitter data.
             It helps classify tweets as either negative or non-negative based on their content, enabling better understanding of
             public opinions and emotions.
             """)

    st.subheader("Data Source")
    st.write("Twitter Tweets Sentiment Dataset ")
    st.write("🔗[**Link to Data Source**](https://www.kaggle.com/datasets/yasserh/twitter-tweets-sentiment-dataset/data)")

    st.subheader("App Content")
    st.write("This app contains multiple sections to guide users through the sentiment analysis process:")
    st.write("1️⃣ **Home:** Provides an overview of the application and its purpose.")
    st.write("2️⃣ **Exploratory Data Analysis (EDA):** Visualizes and explores key trends in the dataset.")
    st.write("3️⃣ **Sentiment Analysis with ML:** Uses machine learning models to predict tweet sentiment based on input data.")
    st.write("4️⃣ **About:** Offers information about the dataset, methodology, and application development.")

def about_page():
    show_banner()
    st.title("About Diabetes Prediction App 📖")

    st.markdown(
        """
        ## 📌 About This App
        This application is a **Diabetes Prediction Tool** built using **Streamlit**. It allows users to assess their risk of developing **early-stage diabetes** using **Machine Learning (ML) models** trained on medical data.  

        The app analyzes user-provided health information and predicts whether the individual has a **high or low risk of diabetes** based on their symptoms and risk factors.
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🔧 Technologies Used")
    st.write("- **Streamlit** for UI and app deployment")
    st.write("- **Scikit-learn** for machine learning model training and inference")
    st.write("- **Pandas & NumPy** for data processing")
    st.write("- **Matplotlib & Seaborn** for data visualization")
    st.write("- **Plotly** for interactive charts")

    st.markdown("## 🎯 Features")
    st.write(
        """
        - **Predict diabetes risk** based on user inputs
        - **Perform exploratory data analysis (EDA)** to understand trends in diabetes-related data
        - **Interactive visualizations** for data insights
        - **User-friendly interface** with real-time processing
        """
    )

    st.markdown("## 👨‍💻 Developer")
    st.write("1️⃣ **Lim Wei Zhen**")
    st.write("2️⃣**Chow Mei Foong**")
    st.write("3️⃣**Chia Zhi Xuan**")
         
    st.markdown("## 💡 How to Use?")
    st.write("1️⃣ Enter relevant health information into the form on the main page.")
    st.write("2️⃣ Click **Predict** to get the diabetes risk assessment.")
    st.write("3️⃣ View the **prediction result** and additional insights.")
    st.write("4️⃣ Click **Reset** to clear the inputs and start over.")

    st.info("""📢 This project is a demonstration of machine learning for diabetes prediction. 
            It is not a medical diagnosis tool. 
            Always consult a healthcare professional for accurate medical assessments.""")