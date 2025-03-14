import streamlit as st

# Libraries for Sentiment Analysis
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Libraries for Data Processing & Data Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Default Wide Screen Mode in Streamlit
st.set_page_config(layout="wide")

# NOTE: Custom HTML + JavaScript to modify the expander text size
st.markdown(
    """
    <style>
    div[data-testid="stExpander"] :not(div[data-testid="stExpanderDetails"] *)  {
    font-size: 16px;
    font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# NOTE: Function to analyze token sentiments
def analyze_sentiments_vader(text):
    
    analyzer = SentimentIntensityAnalyzer()

    pos_lst = []
    neg_lst = []
    neu_lst = []

    for word in text.split():
        res = analyzer.polarity_scores(word)["compound"]

        if res >= 0.1:
            pos_lst.append([word, res])

        elif res <= -0.1:
            neg_lst.append([word, res])
        else:
            neu_lst.append([word])

    result = {"positive": pos_lst, "negative": neg_lst, "neutral": neu_lst}

    # Convert to dataframe
    df_positive = pd.DataFrame(result["positive"], columns=["Word", "Score"]) if result["positive"] else pd.DataFrame(columns=["Word", "Score"])
    df_negative = pd.DataFrame(result["negative"], columns=["Word", "Score"]) if result["negative"] else pd.DataFrame(columns=["Word", "Score"])
    df_neutral = pd.DataFrame(result["neutral"], columns=["Word"]) if result["neutral"] else pd.DataFrame(columns=["Word"])

    # Display the results
    st.write("**Positive Sentiments**", unsafe_allow_html=True)
    st.dataframe(df_positive, hide_index=True, use_container_width=True)
    st.write("**Negative Sentiments**", unsafe_allow_html=True)
    st.dataframe(df_negative, hide_index=True, use_container_width=True)
    st.write("**Neutral Sentiments**", unsafe_allow_html=True)
    st.dataframe(df_neutral, hide_index=True, use_container_width=True) 

def main_page():

    st.title("Sentiment Analysis NLP App")
    st.subheader("A Streamlit Project by Lim Wei Zhen")
    st.write("An app that identifies whether the entered text is **positive, negative, or neutral** and also provides a breakdown of individual words' sentiment scores.")

    # Initialize session state for text area
    if "text_input" not in st.session_state:
        st.session_state["text_input"] = ""

    # Call back function to reset text_input
    def reset_text():
        st.session_state["text_input"] = ""

    # Call back function to update text area state
    def update_text():
        st.session_state["text_input"] = st.session_state["input"]

    # NOTE: How to Use
    st.markdown("### 💡 How to Use?")

    with st.expander("Click here for more information"):
        st.write("1️⃣ Enter text into the input box on the main page.")
        st.write("2️⃣ Click **Analyze Text** to process the sentiment.")
        st.write("3️⃣ View sentiment results and breakdown charts.")
        st.write("4️⃣ Click **Reset** to clear the input and start over.")

    # NOTE: Input
    # Text Area Input for User
    st.markdown("#### Input 📥")

    with st.container(border=True):

        user_input = st.text_area("Enter Text:", st.session_state["text_input"], key="input", on_change=update_text, max_chars=200)

        st.session_state["text_input"] = user_input

        # Button layout
        col1, col2 = st.columns([1,7.5])

        with col1:
            click_button= st.button("Analyze Text", type="primary")
        
        with col2:
            if click_button and len(user_input) > 0:
                st.button("Reset", on_click=reset_text)

    # NOTE: Analysis Results
    # Output for User (Only show after user click on Analyze Text)
    if click_button and len(user_input) > 0:
        st.markdown("#### Analysis Results 📤")

        # Display input text
        st.write("Input Received:")
        st.info(user_input)

        # Create two columns for the analysis results
        col1, col2 = st.columns([2.5, 1.5])

        # Show the polarity & subjectivity, sentiment score, and graphs
        with col1:
            
            with st.expander("Results Breakdown"):
                
                # Get sentiment of the input text
                sentiment = TextBlob(user_input).sentiment

                # Convert the sentiment to DataFrame
                df_sentiment = pd.DataFrame([{
                    "Polarity": sentiment.polarity,
                    "Subjectivity": sentiment.subjectivity
                }])

                # Rename the index
                df_sentiment.index = ["Score"]

                # Transpose the DataFrame
                df_sentiment = df_sentiment.T

                # Display the dataframe
                st.dataframe(df_sentiment, use_container_width=True)

                # Display Sentiment Result
                if sentiment.polarity > 0:
                    st.success("Sentiment: Positive 😁")
                elif sentiment.polarity < 0:
                    st.error("Sentiment: Negative 😢")
                else:
                    st.warning("Sentiment: Neutral 😶")
                
                # Plot Polarity and Subjectivity
                st.write("#### Sentiment Score Breakdown")
                
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(x=df_sentiment.index, y="Score", data=df_sentiment, ax=ax, hue=df_sentiment.index)
                
                ax.set_xlabel("Metrics")

                st.pyplot(fig)

                # Definitions for Polarity and Subjectivity
                st.write("#### ℹ️ Definitions")
                st.write("""
                        **Polarity**  
                        Polarity score is a float within the range of [-1.0, 1.0], where:
                        - Greater than 0.0 is positive sentiment (closer to 1.0 means more positive).
                        - Less than 0.0 is negative sentiment (closer to -1.0 means more negative).
                        - Exactly 0.0 is neutral sentiment, indicating no strong polarity in either direction.
                        """)
                st.write("""
                         **Subjectivity**  
                         Subjectivity is a float within the range of [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
                         """)
                st.write("**Reference**: [Link](https://textblob.readthedocs.io/en/dev/quickstart.html)")
                
        # Show word sentiment
        with col2:
            
            with st.expander("Word Sentiment"):
                
                analyze_sentiments_vader(user_input)


def about_page():
    st.title("📖 About Sentiment Analysis NLP App")

    st.markdown(
        """
        ## 📌 About This App
        This application is a **Sentiment Analysis NLP Tool** built using **Streamlit**. 
        It allows users to analyze the sentiment of a given text using **TextBlob** and **VADER (Valence Aware Dictionary and sEntiment Reasoner)**.
        
        The app identifies whether the entered text is **positive, negative, or neutral** and also provides a breakdown of individual words' sentiment scores.
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🔧 Technologies Used")
    st.write("- **Streamlit** for UI and deployment")
    st.write("- **TextBlob** for sentiment analysis")
    st.write("- **VADER Sentiment Analysis** for token-level sentiment analysis")
    st.write("- **Matplotlib & Seaborn** for data visualization")
    st.write("- **Pandas** for data processing")

    st.markdown("## 🎯 Features")
    st.write(
        """
        - **Analyze sentiment of user-input text**
        - **Visualize polarity and subjectivity scores**
        - **Break down individual word sentiments using VADER**
        - **User-friendly interface with real-time processing**
        """
    )

    st.markdown("## 👨‍💻 Developer")
    st.write("**Developed by: Lim Wei Zhen**")
    st.write("**GitHub:** [Link](https://github.com/WeiZhenLim/MachineLearning_DeepLearning_Projects/tree/main/04-Simple_Sentiment_Analysis_NLP_App)")
    st.write("**LinkedIn:** [Link](https://www.linkedin.com/in/weizhen-lim/)")

    st.markdown("## 📚 Learning Resources")
    st.write(
        """
        This project was built using knowledge gained from the Udemy course:  
        **[Streamlit for Data Science and Machine Learning](https://www.udemy.com/share/103Mg23@lrrcYB5c9ZvznO0Oc6LD691ZFuIsmh_HumMlHZcZ6GyBZXxSC7va-YKFuym8XZWi2g==/)**  
        """
    )
    st.write("**Instructor:** Jesse E. Agbe [(Link to Bio)](https://www.udemy.com/user/jesse-e-agbe/)")

    st.markdown("## 💡 How to Use?")
    st.write("1️⃣ Enter text into the input box on the main page.")
    st.write("2️⃣ Click **Analyze Text** to process the sentiment.")
    st.write("3️⃣ View sentiment results and breakdown charts.")
    st.write("4️⃣ Click **Reset** to clear the input and start over.")

    st.info("📢 This project is a demonstration of NLP sentiment analysis using Streamlit. More enhancements will be added in future updates!")

# Create Page
main_pg = st.Page(main_page, title="Sentiment Analysis NLP App", icon="😶‍🌫️")
about_pg = st.Page(about_page, title="About", icon="📖")

# Create Navigation
nav = st.navigation([main_pg, about_pg])
nav.run()