import streamlit as st

# Import NLP libraries
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.util import bigrams, trigrams
from spellchecker import SpellChecker
from Levenshtein import distance

# Import Language Tool
import language_tool_python

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

# NOTE: Initialize LanguageTool (English)
lt_tool = language_tool_python.LanguageToolPublicAPI("en-US")

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

# NOTE: Build a Bigram & Trigram Model
# Initialize bigram and trigram frequency dictionaries
bigram_counts = defaultdict(int)
trigram_counts = defaultdict(int)

# Create bigram and trigram models from tokenized words
for w1, w2 in bigrams(tokens):
    bigram_counts[(w1, w2)] += 1

for w1, w2, w3 in trigrams(tokens):
    trigram_counts[(w1, w2, w3)] += 1

def get_bigram_probability(prev_word, word):
    
    if (prev_word, word) in bigram_counts:
        return bigram_counts[(prev_word, word)] / sum(bigram_counts.values())
    return 0  # If bigram not found, return 0 probability

def get_trigram_probability(prev_word, word, next_word):
    
    if (prev_word, word, next_word) in trigram_counts:
        return trigram_counts[(prev_word, word, next_word)] / sum(trigram_counts.values())
    return 0  # If trigram not found, return 0 probability

# NOTE: Main Spell Checker Functions

# Initialize SpellChecker
spell = SpellChecker()
spell.word_frequency.load_words(list(word_freq.keys()))  # Load Reuters words

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

# Function to detect real-world spelling errors using LanguageTool + N-grams
def detect_real_word_errors(text, top_n=5):
    matches = lt_tool.check(text)
    real_word_errors = {}

    # Store errors detected by LanguageTool
    for match in matches:
        # Extract the incorrect word using context and offset
        error_word = text[match.offset : match.offset + match.errorLength].strip()
        
        # Ensure the extracted word is valid and not already added
        if error_word and error_word not in real_word_errors:
            real_word_errors[error_word] = match.replacements[:top_n]  # Store top 'n' suggestions

    # Check for unusual word sequences using Bigram & Trigram probabilities
    words = text.split()
    for i, word in enumerate(words):
        prev_word = words[i - 1] if i > 0 else None
        next_word = words[i + 1] if i < len(words) - 1 else None

        if word in real_word_errors:  # Skip if already detected by LanguageTool
            continue

        # Compute probabilities
        bigram_prob = get_bigram_probability(prev_word, word)
        trigram_prob = get_trigram_probability(prev_word, word, next_word)

        # If both probabilities are **very low**, flag as real-word error
        if bigram_prob < 0.001 and trigram_prob < 0.0005:  # Adjust thresholds based on corpus
            try:
                real_word_errors[word] = list(spell.candidates(word))[:top_n] or [''] # Use spellchecker for suggestions
            except Exception as e:
                real_word_errors[word] = ['']

    return real_word_errors

# Function to suggest corrections with optional bigram & trigram probability ranking
def suggest_corrections(word, prev_word=None, next_word=None, top_n=5):

    original_word = word  # Store original word
    word = word.lower().strip(".,!?")  # Normalize word for lookup
    
    try:
        candidates = list(spell.candidates(word)) or ['']
    except Exception as e:
        print(f"Error: {e} | Problematic word: '{word}'")
        candidates = ['']  # Return an empty list instead of failing

    # If there's a previous word, rank suggestions using bigram probabilities
    if prev_word or next_word:
        candidates = sorted(
            candidates,
            key=lambda w: (
                distance(word, w),
                -word_freq.get(w, 0),  # Prioritize common words in Reuters
                -bigram_counts.get((prev_word, w), 0),
                -trigram_counts.get((prev_word, w, next_word), 0) if prev_word and next_word else 0  # Trigram probability
                )
        )

    return candidates[:top_n]

# Function to detect and suggest corrections in one step
def detect_and_suggest_corrections(text, top_n=5):

    # Extract original words as they appear in the input text
    words_original = re.findall(r"\b\w+['-]?\w*\b", text)
    
    # Normalize words to lowercase for SpellChecker lookup
    words_normalized = [word.lower().strip(".,!?") for word in words_original]

    # Detect non-word spelling errors
    misspelled_words = detect_misspellings(text) 
    
    # Detect real-world errors using LanguageTool
    real_word_errors = detect_real_word_errors(text)
    
    corrections = {}

    for i, word in enumerate(words_original):
        normalized_word = words_normalized[i]  # Get the corresponding normalized word
        prev_word = words_original[i - 1] if i > 0 else None  # Get the previous word
        next_word = words_original[i + 1] if i < len(words_original) - 1 else None  # Get the next word

        # Handle non-word spelling errors using SpellChecker
        if word in misspelled_words:
            corrections[word] = suggest_corrections(normalized_word, prev_word, next_word, top_n)
        
        # Handle real-word errors using LanguageTool
        elif word in real_word_errors:
            corrections[word] = real_word_errors[word]

    print("Misspelled word:")
    print(misspelled_words)
    print("Real-world error:")
    print(real_word_errors.keys())
    print("Corrections:")
    print(corrections)

    return misspelled_words + list(real_word_errors.keys()), corrections

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
    test_text = """
                The stock market experienced high volitility this week, affecting major indexes. 
                An invstor sold off shares in tech companies due to fear of a downturn. 
                The bond sell rate increased, and many traders adjusted their principal strategies accordingly. 
                Analysts recommend holding positions despite short-term movements.
                """
    detect_and_suggest_corrections(test_text)
    pass