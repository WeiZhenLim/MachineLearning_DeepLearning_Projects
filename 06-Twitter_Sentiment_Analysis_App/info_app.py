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
    st.title("About This App 📌")

    st.markdown(
        """
        This application is a **Twitter Sentiment Analysis Tool** built using **Streamlit** and powered by **Machine Learning (ML)**.
        The app analyzes user-submitted tweets and classifies them into two categories:  
        - **Negative**
        - **Non-Negative (Neutral/Positive)** 
        
        It's designed to showcase the use of NLP techniques and ML models in real-time sentiment classification. 
        The classification is powered by a fine-tuned **XGBoost model**, and text is preprocessed and vectorized using **TF-IDF**.
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔧 Technologies Used")
    st.write("- **Streamlit** for UI and web app deployment")
    st.write("- **Scikit-learn & XGBoost** for machine learning modeling")
    st.write("- **NLTK & Regex** for text preprocessing")
    st.write("- **TF-IDF Vectorizer** for feature extraction")
    st.write("- **Plotly & Matplotlib** for interactive visualizations")
    st.write("- **Pandas & NumPy** for data manipulation")

    st.subheader("🎯 Features")
    st.write(
        """
        - **Predict sentiment** of tweets using a trained XGBoost model
        - **Preprocessing pipeline** including tokenization, cleaning, and vectorization
        - **Interactive interface** with clean UI and real-time feedback
        - **View prediction tweet sentiment and cleaned tweet input**
        """
    )

    st.subheader("👨‍💻 Team Members")
    st.write("1️⃣ **Chow Mei Foong**")
    st.write("2️⃣ **Lim Wei Zhen**")
    st.write("3️⃣ **Chia Zhi Xuan**")
         
    st.subheader("💡 How to Use?")
    st.write("1️⃣ Enter a tweet into the input box on the Twitter Tweets Sentiment Analysis page.")
    st.write("2️⃣ Click **Check Tweet Sentiment** to process and classify the input.")
    st.write("3️⃣ View the **cleaned text for sentiment analysis** and the **prediction tweets sentiment**.")
    st.write("4️⃣ Use **Reset** to clear the form and try again.")

    st.subheader("Future Work 🚀")
    st.write("1️⃣ Improve Text Preprocessing – Some sentiment-bearing words were not processed correctly. The preprocessing pipeline should be reviewed to better handle context, punctuation, and special cases.")
    st.write("2️⃣ Enable Multiclass Classification – Currently, neutral and positive tweets are grouped. Future work can explore predicting negative, neutral, and positive sentiments separately.")
    st.write("3️⃣ Explore Deep Learning Models – Future improvements could include using models like LSTM or BERT for better contextual understanding and prediction accuracy.")