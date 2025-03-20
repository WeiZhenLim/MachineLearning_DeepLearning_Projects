import streamlit as st

# Import NLP libraries
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.util import bigrams, trigrams
from spellchecker import SpellChecker
from Levenshtein import distance

# Data Visualization
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from collections import Counter, defaultdict
import re

# Ensure necessary downloads
nltk.download('punkt_tab')
nltk.download("punkt")
nltk.download("reuters")
nltk.download("words")
nltk.download("stopwords")
nltk.download('wordnet')

# ------------------------------------------------------------------------------------------------------------------------------

# NOTE: Load corpus data, words, and stopwords

# Load Reuters corpus safely
from nltk.corpus import reuters, words, stopwords

# Verify Reuters corpus availability
if not reuters.fileids():
    raise RuntimeError("Reuters corpus is missing or corrupted. Try re-downloading using `nltk.download('reuters')`.")

# Load all words from Reuters corpus
reuters_words = reuters.words()

# Load English dictionary words to filter out non-words
english_vocab = set(words.words())

# Load common stopwords to prevent false positives
stop_words = set(stopwords.words("english"))

# NOTE: Preprocessing steps to clean and prepare the Reuters dataset

# Step 1: Convert Text to Lowercase
reuters_words = " ".join([word.lower() for word in reuters_words])

# Step 2: Tokenization
tokens = word_tokenize(reuters_words)

# Step 3: Remove punctuation & special characters
tokens = [word for word in tokens if word.isalnum()]

# Step 4: Remove stopwords
tokens = [word for word in tokens if word not in stop_words]

# Step 5: Remove words that are not in a valid dictionary
tokens = [word for word in tokens if word in english_vocab]

# Step 6: Lemmatization (Reduce Words to Base Form)
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(word) for word in tokens]

# Step 7: Frequency Distribution of Words for Reuters corpus dataset
word_freq = Counter(tokens)

# NOTE: Build a Bigram Model & Trigram Model

# Bigram Model with Laplace Smoothing
bigram_counts = Counter(bigrams(tokens))
bigram_word_counts = Counter(tokens) # Frequency of individual words

# Trigram Model with Laplace Smoothing
trigram_counts = Counter(trigrams(tokens))
bigram_pair_counts = Counter(bigrams(tokens)) # Frequency of individual words

# Get Vocabulary Size for Smoothing
V = len(word_freq)

# Function to get Bigram Probability with Smoothing
def get_bigram_prob(w1, w2):
    return (bigram_counts.get((w1, w2), 0) + 1) / (bigram_word_counts.get(w1, 0) + V)

# Function to get Trigram Probability with Smoothing
def get_trigram_prob(w1, w2, w3):
    return (trigram_counts.get((w1, w2, w3), 0) + 1) / (bigram_pair_counts.get((w1, w2), 0) + V)

# NOTE: Main Spell Checker Functions

# Initialize SpellChecker
spell = SpellChecker()
spell.word_frequency.load_words(list(word_freq.keys()))  # Load Reuters words

# Function to detect misspelled words while preserving original input formatting
def detect_misspellings(text):
    # Extract words while keeping their original form
    words = re.findall(r"\b\w+['-]?\w*\b", text)  # Keeps contractions & hyphenated words

    # Normalize words to lowercase for SpellChecker lookup
    normalized_words = [word.lower().strip(".,!?-") for word in words]

    # Find misspelled words using normalized text
    unknown_words = spell.unknown(normalized_words)

    # Return original words from the input (not the normalized version)
    misspelled_words = [words[i] for i, norm_word in enumerate(normalized_words) if norm_word in unknown_words]

    return misspelled_words

# Function to suggest corrections with optional bigram probability ranking
def suggest_corrections(word, prev_word=None, next_word=None, top_n=5):

    word = word.lower().strip(".,!?-")  # Normalize word for lookup
    
    try:
        candidates = list(spell.candidates(word)) or ['']
    except Exception as e:
        print(f"Error: {e} | Problematic word: '{word}'")
        candidates = ['']  # Return an empty list instead of failing

    # If there's a previous word or next word, rank suggestions using bigram probabilities
    if prev_word:
        candidates = sorted(
            candidates,
            key=lambda w: (
                distance(word, w),
                -word_freq.get(w, 0),  # Prioritize common words in Reuters
                -get_bigram_prob(prev_word, w) if prev_word else 0,
                -get_trigram_prob(prev_word, w, next_word) if prev_word and next_word else 0
                )
        )

    return candidates[:top_n]

# Function to detect and suggest corrections in one step
def detect_and_suggest_corrections(text, top_n=5):

    # Extract original words as they appear in the input text
    words_original = re.findall(r"\b\w+['-]?\w*\b", text)
    
    # Normalize words to lowercase for SpellChecker lookup
    words_normalized = [word.lower().strip(".,!?-") for word in words_original]

    misspelled_words = detect_misspellings(text)  # Detect misspelled words
    corrections = {}

    for i, word in enumerate(words_original):
        normalized_word = words_normalized[i]  # Get the corresponding normalized word
        prev_word = words_original[i - 1] if i > 0 else None # Get the previous word
        next_word = words_original[i + 1] if i < len(words_original) - 1 else None  # Get the next word

        if word in misspelled_words:
            corrections[word] = suggest_corrections(normalized_word, prev_word, next_word, top_n)

    # Store words that need to be removed
    words_to_remove = [word for word, corr in corrections.items() if corr[0] == '']

    # Remove from dictionary and list
    for word in words_to_remove:
        del corrections[word]  # Remove from dictionary
        if word in misspelled_words:
            misspelled_words.remove(word)  # Remove from the list

    return misspelled_words, corrections

# NOTE: Data Viz Functions
# Top N Most Frequent Words
def plot_top_n_most_frequent_words(n, figsize_tup):
    # Select top N most frequent words
    most_common_words = word_freq.most_common(n)

    # Extract words and frequencies for plotting
    words, frequencies = zip(*most_common_words)

    # Plot a bar chart
    plt.figure(figsize=figsize_tup)
    plt.bar(words, frequencies)
    plt.title(f"Top {n} Most Frequent Words in Reuters Corpus")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    
    return plt

# Document Category Distribution 
def plot_doc_cat_dis(n, figsize_tup):

    # Get category distribution
    categories = reuters.categories()
    category_counts = {cat: len(reuters.fileids(cat)) for cat in categories}

    # Select top 10 categories
    top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:n]
    labels, sizes = zip(*top_categories)

    # Plot Pie Chart
    plt.figure(figsize=figsize_tup)
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Top {n} Reuters Categories by Number of Articles")
    plt.tight_layout()
    
    return plt

# Document Length Histogram
def plot_doc_length_hist(figsize_tup, num_bins):
    # Get document lengths
    doc_lengths = [len(reuters.raw(file_id)) for file_id in reuters.fileids()]

    # Plot Histogram
    plt.figure(figsize=figsize_tup)
    plt.hist(doc_lengths, bins=int(num_bins), edgecolor='black')
    plt.xlabel("Document Length (Word Count)")
    plt.ylabel("Number of Articles")
    plt.title("Distribution of Document Lengths in Reuters Dataset")
    
    return plt

# Word Cloud
def plot_word_cloud(width, height, figsize_tup):

    # Generate Word Cloud
    wordcloud = WordCloud(width=width, height=height, background_color='white').generate(" ".join(tokens))

    # Plot Word Cloud
    plt.figure(figsize=figsize_tup)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of Reuters Dataset")
    
    return plt


# NOTE: Debug function
# Function to check if words exist in the Reuters corpus
def check_words_in_corpus(words_to_check, word_freq):
    missing_words = []
    
    for word in words_to_check:
        word_lower = word.lower()  # Ensure lowercase comparison
        if word_freq.get(word_lower, 0) == 0:
            missing_words.append(word_lower)

    if missing_words:
        print(f"Warning: The following words are missing or have zero frequency in the corpus: {missing_words}")
    else:
        print("All words exist in the corpus with valid frequency.")

if __name__ == "__main__":
    # test_text = """
    #             Incvestors are always looking for stable markets, but recent tranactions show high reccesion risks. 
    #             The stock market’s volitality has increased due to inflattion concerns. 
    #             Many firms are struggling to avoid bankrupty as interest rates rise. 
    #             Experts suggest diversifying assets to mitigate risk. 
    #             The central bank’s policies could stabilize the economy, but uncertainty remains high in global financial sectors.
    #             """
    # detect_and_suggest_corrections(test_text)

    # Check whether 
    plot_word_cloud(500, 600, (15, 6))
    plot_doc_cat_dis(10, (15, 12))
    plot_doc_length_hist((15, 6), 30)
    plot_top_n_most_frequent_words(10, (15, 12))
    pass