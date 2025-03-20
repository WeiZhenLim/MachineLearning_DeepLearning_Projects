import streamlit as st

# Import NLP libraries
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
from spellchecker import SpellChecker
from Levenshtein import distance

from collections import Counter, defaultdict
import re

# Ensure necessary downloads
nltk.download("punkt")
nltk.download("reuters")
nltk.download("words")
nltk.download("stopwords")

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

# NOTE: Build a Bigram Model
bigram_counts = defaultdict(int)
for w1, w2 in bigrams(tokens):
    bigram_counts[(w1, w2)] += 1

# NOTE: Main Spell Checker Functions

# Initialize SpellChecker
spell = SpellChecker()
spell.word_frequency.load_words(list(word_freq.keys()))  # Load Reuters words

# Add Custom Word List
spell.word_frequency.load_words(["cutting-edge"])

# Function to detect misspelled words while preserving original input formatting
def detect_misspellings(text):
    # Extract words while keeping their original form
    words = re.findall(r"\b\w+['-]?\w*\b", text)  # Keeps contractions & hyphenated words

    # Normalize words to lowercase for SpellChecker lookup
    normalized_words = [word.lower().strip(".,!?") for word in words]

    # Find misspelled words using normalized text
    unknown_words = spell.unknown(normalized_words)

    # Return original words from the input (not the normalized version)
    misspelled_words = [words[i] for i, norm_word in enumerate(normalized_words) if norm_word in unknown_words]

    return misspelled_words

# Function to suggest corrections with optional bigram probability ranking
def suggest_corrections(word, prev_word=None, top_n=5):

    original_word = word  # Store original word
    word = word.lower().strip(".,!?")  # Normalize word for lookup
    
    try:
        candidates = list(spell.candidates(word)) or ['']
    except Exception as e:
        print(f"Error: {e} | Problematic word: '{word}'")
        candidates = ['']  # Return an empty list instead of failing

    # If there's a previous word, rank suggestions using bigram probabilities
    if prev_word:
        candidates = sorted(
            candidates,
            key=lambda w: (
                distance(word, w),
                -word_freq.get(w, 0),  # Prioritize common words in Reuters
                -bigram_counts.get((prev_word, w), 0)
                )
        )

    return candidates[:top_n]

# Function to detect and suggest corrections in one step
def detect_and_suggest_corrections(text, top_n=5):

    # Extract original words as they appear in the input text
    words_original = re.findall(r"\b\w+['-]?\w*\b", text)
    
    # Normalize words to lowercase for SpellChecker lookup
    words_normalized = [word.lower().strip(".,!?") for word in words_original]

    misspelled_words = detect_misspellings(text)  # Detect misspelled words
    corrections = {}

    for i, word in enumerate(words_original):
        normalized_word = words_normalized[i]  # Get the corresponding normalized word

        if word in misspelled_words:
            prev_word = words_original[i - 1] if i > 0 else None  # Get the previous word
            corrections[word] = suggest_corrections(normalized_word, prev_word, top_n)

    return misspelled_words, corrections

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
    pass