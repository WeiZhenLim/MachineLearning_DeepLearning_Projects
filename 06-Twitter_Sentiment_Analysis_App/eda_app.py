import streamlit as st

# Load EDA Packages
import pandas as pd
import re
from collections import Counter
from nltk.corpus import stopwords
import string

# Load Data Viz Packages
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

# Load utils
from utils import show_banner, expander_formatter

# NOTE: Functions
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

# NOTE: Apps
def eda_des_page():
    show_banner()
    st.title("Exploratory Data Analysis 🔍")

    st.subheader("Summary Statistics 📑")
    st.write("This section provides a descriptive analysis of the Twitter Tweets dataset.")

    # Load dataset
    df = load_data("data/Tweets.csv")
    df.dropna(inplace=True) # Drop record with missing value
    df_processed = load_data("data/Preprocessed_Tweets.csv")

    # Format expander font size
    expander_formatter(16)

    with st.expander("Overview of Raw Data"):       
        st.dataframe(df, height=250)

    with st.expander("Sentiment Distribution"): 
        st.dataframe(df['sentiment'].value_counts(), use_container_width=True)

        st.warning("""For this project, to simplify the classification task, neutral and positive tweets are combined into a single category - ***non-negative***.
                   This results in a binary sentiment classification: ***negative*** vs. ***non-negative***.
                   """)

    with st.expander("Sentiment Distribution (After Label Grouping)"):
        st.dataframe(df_processed['sentiment'].value_counts(), use_container_width=True)

        st.warning("""After label grouping, the sentiment distribution became significantly imbalanced. Therefore, a class balancing technique (SMOTE)
                   will be applied during model development.
                   """)

    with st.expander("Descriptive Statistics of Tweets Length"):
        # Calculate tweet length by word counts
        df['tweet_length_words'] = df['text'].apply(lambda x: len(x.split()))
        st.write("**Tweet Length (Word Count)**")
        st.dataframe(df['tweet_length_words'].describe().drop('count'), use_container_width=True)

        # Calculate tweet length by characters
        df['tweet_length_chars'] = df['text'].apply(len)
        st.write("**Tweet Length (Characters)**")
        st.dataframe(df['tweet_length_chars'].describe().drop('count'), use_container_width=True)

    with st.expander("Distributions of Hashtags and Mentions"):
        # Extract hashtags and mentions
        df['hashtags'] = df['text'].apply(lambda x: re.findall(r'#\w+', x))
        df['mentions'] = df['text'].apply(lambda x: re.findall(r'@\w+', x))

        # Count hashtags and mentions
        all_hashtags = [tag.lower() for tags in df['hashtags'] for tag in tags]
        all_mentions = [mention.lower() for mentions in df['mentions'] for mention in mentions]

        hashtag_counts = Counter(all_hashtags)
        mention_counts = Counter(all_mentions)

        hashtags_df = pd.DataFrame(hashtag_counts.most_common(10), columns=['Hashtag', 'Count'])
        mentions_df = pd.DataFrame(mention_counts.most_common(10), columns=['Mention', 'Count'])

        st.write("**Top 10 Commonly Used Hashtags**")
        st.dataframe(hashtags_df, use_container_width=True, hide_index=True)
        st.write("**Top 10 Commonly Used Mentions**")
        st.dataframe(mentions_df, use_container_width=True, hide_index=True)

        st.warning("""Both hashtags and mentions are considered noise for the development of the text classification model.
                   They will be removed during the data preprocessing steps.
                   """)

    with st.expander("Distributions of Stopwords and Punctuations"):
        # Define stopwords and punctuation
        stop_words = set(stopwords.words('english'))
        punctuations = set(string.punctuation)

        stopword_counts = Counter()
        punctuation_counts = Counter()

        for tweet in df['text']:
            words = tweet.split()
            stopword_counts.update([word.lower() for word in words if word.lower() in stop_words])
            punctuation_counts.update([char for char in tweet if char in punctuations])

        stopword_df = pd.DataFrame(stopword_counts.most_common(20), columns=['Stopword', 'Count'])
        punctuation_df = pd.DataFrame(punctuation_counts.most_common(10), columns=['Punctuation', 'Count'])

        st.write("**Top 20 Commonly Used Stopwords**")
        st.dataframe(stopword_df, use_container_width=True, hide_index=True)
        st.write("**Top 10 Commonly Used Punctuations**")
        st.dataframe(punctuation_df, use_container_width=True, hide_index=True)

        st.warning("""Both stopwords and punctuations are considered noise for the development of the text classification model.
                   They will be removed during the data preprocessing steps.
                   """)

def eda_plot_page():
    show_banner()
    st.title("Exploratory Data Analysis 🔍")

    st.subheader("Data Visualization 📊")
    st.write("This section provides various data visualization plots to help understand the Twitter Tweets dataset.")

    # Load dataset
    df = load_data("data/Tweets.csv")
    df.dropna(inplace=True) # Drop record with missing value
    df_processed = load_data("data/Preprocessed_Tweets.csv")

    # Format expander font size
    expander_formatter(16)

    # Custom Color Mapping
    color_map = {
        'positive': '#77DD77',   # light green
        'negative': '#FF6961',   # soft red
        'neutral': '#FDFD96',     # pastel yellow
        'non-negative': '#ADD8E6'
    }

    with st.expander("Sentiment Distribution"):

        sentiment_df = df["sentiment"].value_counts().reset_index()
        sentiment_df.columns = ["Sentiment", "Count"]

        p1 = px.pie(sentiment_df, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map)
        st.plotly_chart(p1, use_container_width=True)

    with st.expander("Sentiment Distribution (After Label Grouping)"):

        sentiment_df = df_processed["sentiment"].value_counts().reset_index()
        sentiment_df.columns = ["Sentiment", "Count"]

        p2 = px.pie(sentiment_df, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map)
        st.plotly_chart(p2, use_container_width=True)

    with st.expander("Tweet Length Distribution"):
        # Calculate tweet length by word counts
        df['tweet_length_words'] = df['text'].apply(lambda x: len(x.split()))
        st.write("**Tweet Length (Word Count)**")
        p3 = px.histogram(df, x='tweet_length_words', opacity=0.5)
        p3.update_traces(marker_line_color='black', marker_line_width=1)
        st.plotly_chart(p3, use_container_width=True)

        # Calculate tweet length by characters
        df['tweet_length_chars'] = df['text'].apply(len)
        st.write("**Tweet Length (Characters)**")
        p4 = px.histogram(df, x='tweet_length_chars', opacity=0.5)
        p4.update_traces(marker_line_color='black', marker_line_width=1)
        st.plotly_chart(p4, use_container_width=True)

    with st.expander("WordCloud (Before Data Preprocessing)"):
        # Combine positive and neutral sentiment into one class, i.e. non-negative
        df['sentiment'] = df['sentiment'].replace({'neutral': 'non-negative', 'positive': 'non-negative'})

        # Function to generate a WordCloud for a given sentiment
        def generate_wordcloud(df, sentiment, text_type):
            text = " ".join(df[(df['sentiment'] == sentiment) & (df[text_type].apply(lambda x: isinstance(x, str)))][text_type])
            wordcloud = WordCloud(width=600, height=300, background_color="white").generate(text)

            # Display the word cloud
            fig = plt.figure(figsize=(8, 4))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title(f"WordCloud for {sentiment.capitalize()} Sentiment", fontsize=12)
            st.pyplot(fig)

        generate_wordcloud(df, "negative", "text")
        generate_wordcloud(df, "non-negative", "text")

    with st.expander("WordCloud (After Data Preprocessing)"):
        generate_wordcloud(df_processed, "negative", "stemmed_text")
        generate_wordcloud(df_processed, "non-negative", "stemmed_text")