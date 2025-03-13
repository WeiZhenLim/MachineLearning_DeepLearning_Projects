import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def main_page():

    st.title("Sentiment Analysis NLP App")
    st.subheader("A Streamlit Project by Lim Wei Zhen")

    # Initialize session state for text area
    if "text_input" not in st.session_state:
        st.session_state["text_input"] = ""

    # Call back function to reset text_input
    def reset_text():
        st.session_state["text_input"] = ""

    # Call back function to update text area state
    def update_text():
        st.session_state["text_input"] = st.session_state["input"]

    # NOTE: Input
    # Text Area Input for User
    st.markdown("#### Input 📥")

    with st.container(border=True):

        user_input = st.text_area("Enter Text:", st.session_state["text_input"], key="input", on_change=update_text, max_chars=200)

        st.session_state["text_input"] = user_input

        # Button layout
        col1, col2 = st.columns([1,4.8])

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
                st.dataframe(df_sentiment)

                # Display Sentiment Result
                if sentiment.polarity > 0:
                    st.success("Sentiment: Positive 😁")
                elif sentiment.polarity < 0:
                    st.error("Sentiment: Negative 😢")
                else:
                    st.warning("Sentiment: Neutral 😶")

                # Plot Polarity and Subjectivity
                st.subheader("Sentiment Score Breakdown")
                
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(x=df_sentiment.index, y="Score", data=df_sentiment, ax=ax, hue=df_sentiment.index)
                
                ax.set_xlabel("Metrics")

                st.pyplot(fig)
                
        # Show word sentiment
        with col2:
            
            with st.expander("Word Sentiment"):
                st.write("Results")

            pass


def about_page():
    pass

# Create Page
main_pg = st.Page(main_page, title="Sentiment Analysis NLP App", icon="😶‍🌫️")
about_pg = st.Page(about_page, title="About", icon="📖")

# Create Navigation
nav = st.navigation([main_pg, about_pg])
nav.run()