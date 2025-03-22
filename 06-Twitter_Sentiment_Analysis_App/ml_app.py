import streamlit as st

# Load ML Packages
import joblib
import os
import requests
from io import BytesIO

# Load EDA Packages
import numpy as np
import pandas as pd

# Load Data Preprocessing Packages
import re
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk

# Load utils 
from utils import show_banner, expander_formatter
import time

# NOTE: Function to Load ML MOdels
@st.cache_resource
def load_model(model_file):
    response = requests.get(model_file)
    loaded_model = joblib.load(BytesIO(response.content))
    return loaded_model

# Download stopwords from nltk
nltk.download("stopwords")

# URL from github
url_vec = "https://raw.githubusercontent.com/WeiZhenLim/MachineLearning_DeepLearning_Projects/main/06-Twitter_Sentiment_Analysis_App/model/20250322_TFIDFVectorizer.pkl"
url_model = "https://raw.githubusercontent.com/WeiZhenLim/MachineLearning_DeepLearning_Projects/main/06-Twitter_Sentiment_Analysis_App/model/20250322_Tuned_XGBoost_Model.pkl"

# Function to preprocess the input text
def preprocess_text(text):

    # Emoticons Handling
    # Define positive and negative emoticons
    positive_emoticons = {":)", ":D", "XD", ":-)", "=)", ":-D", "(:", "(-:", ": D", ";D", ";-D", "(;", "(-;", "<3", "^-^", "^_^", "=D" }
    negative_emoticons = {":(", ":-(", ":**-(", ":@", ":-@", ":\\", ":-\\", ":,(", ":'(" }

    for emo in positive_emoticons:
        text = re.sub(re.escape(emo), "emo_happy", text)
    for emo in negative_emoticons:
        text = re.sub(re.escape(emo), "emo_sad", text)

    # Convert Text to Lowercase
    text = " ".join(word.lower() for word in text.split())

    # Conversion of Common Abbreviations
    # Common abbreviations
    abbreviation_dict = {
        "lol": "laughing out loud",
        "omg": "oh my god",
        "jk": "just kidding",
        "lmao": "laughing my ass off",
        "idk": "i don't know",
        "brb": "be right back",
        "btw": "by the way",
        "ttyl": "talk to you later",
        "imo": "in my opinion",
        "tbh": "to be honest",
        "u": "you",
        "tks": "thanks",
        "thnx": "thanks",
        "thks": "thanks"
    }
    text = " ".join([abbreviation_dict[word.lower()] if word.lower() in abbreviation_dict else word for word in text.split()])

    # Reduction of Repetitive Letters
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # Removing Noise (URL, Punctuations, Hashtags, Mentions, etc.)
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)  # Remove mentions (@user)
    text = re.sub(r"#\w+", "", text)  # Remove hashtags (#topic)

    punctuation_to_remove = string.punctuation.replace("!", "").replace("?", "")  # Remove all punctuation except ! and ?
    text = text.translate(str.maketrans('', '', punctuation_to_remove))

    text = re.sub(r'\.{2,}', '.', text)  # Replace multiple dots ".." or "..." with a single dot
    text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space

    # Stopwords Removal
    stop_words = set(stopwords.words('english')) - {"not", "no", "never", "don't", "won't", "isn't", "wasn't", "but", "although", "why", "how", "what", "who", "where", "when"}
    text = " ".join([word for word in text.split() if word not in stop_words])

    # Tokenization
    text = text.split()

    # Stemming
    stemmer = PorterStemmer()
    text = [stemmer.stem(word) for word in text]

    # Join the stemmed text into a string
    text = " ".join(text)

    # Vectorization
    vectorizer = load_model(url_vec)
    text_vec = vectorizer.transform([text])

    return text, text_vec

# NOTE: ML Page
def ml_page():
    show_banner()
    st.title("Twitter Tweets Sentiment Analysis with Machine Learning 🤖")
    st.write("Analyze the sentiment of any tweet using a machine learning model trained on Twitter Tweets data.")

    st.subheader("Input 📥")

    # Initialize session state for reset button
    if "reset_triggered" not in st.session_state:
        st.session_state["reset_triggered"] = False

    # Reset logic
    if st.session_state["reset_triggered"]:
        st.session_state["input_text"] = ""
        st.session_state["reset_triggered"] = False
        st.rerun()

    # Input
    with st.container(border=True):
        
        input_text = st.text_area(label="Enter your tweet here (500 characters limit):", max_chars=500, key="input_text")

        # Button Layout
        col1, col2 = st.columns([1, 2.5])
        
        with col1:
            submit_info = st.button("Check Tweet Sentiment")

        with col2:
            reset = st.button("Reset")

    # Reset
    if reset:
        st.session_state["reset_triggered"] = True
        st.rerun()

    # Actions After Click Check Tweet Sentiment Button
    if submit_info and len(input_text) > 0:
        
        # Add spinner
        with st.spinner("Checking for tweet sentiment...", show_time=True):
            time.sleep(2)
            st.toast("Sentiment analysis complete!", icon="✅")

        expander_formatter(16)

        st.subheader("Tweet Sentiment Breakdown 🗣️")

        # Processed Input for ML
        text_no_vec, single_sample = preprocess_text(input_text)

        with st.expander("Cleaned Tweet for Prediction"):
            st.write("Your tweet, prepped for analysis:")
            st.info(text_no_vec)

        # Prediction Result
        with st.expander("Final Sentiment Prediction"):

            model = load_model(url_model)

            pred_prob = model.predict_proba(single_sample)[0][1]

            prediction = (pred_prob >= 0.3).astype(int)
            
            if prediction == 1:
                st.error("🙁 Hmm... this tweet sounds a bit negative.")
                st.write("ℹ️Maybe it’s expressing frustration, concern, or disagreement.")
            else:
                st.success("😄 This tweet seems non-negative!")
                st.write("ℹ️It's either positive or neutral in tone — nothing too harsh here.")
    
    elif submit_info and len(input_text) == 0:
        st.error("⚠️ Please enter a tweet before checking its sentiment.")