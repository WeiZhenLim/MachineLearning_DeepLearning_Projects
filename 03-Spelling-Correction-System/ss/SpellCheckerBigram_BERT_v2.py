import streamlit as st

# Import NLP libraries
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
from spellchecker import SpellChecker
from Levenshtein import distance 

# BERT Model
from transformers import pipeline
from torch import Tensor

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

# NOTE: Load the pre-trained BERT model for fill-mask tasks
bert_corrector = pipeline("fill-mask", model="bert-base-uncased")

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

# NOTE: Functions for Detections
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

# Function to detect context-based errors using BERT
def is_real_word_error(prev_word, word, next_word, full_text, threshold=0.2):

    bert_suggestions, confidence_scores = get_bert_suggestions(word, prev_word, next_word, full_text)

    if not bert_suggestions:
        return False  # If no suggestions, assume it's correct

    top_suggestion = bert_suggestions[0]
    top_confidence = confidence_scores[0] if confidence_scores else 1.0  # Default confidence to 1.0

    # Check if the suggested word is **too different** from the original word
    word_difference = distance(word, top_suggestion)

    # Only flag as an error if:
    if (
        top_confidence < threshold  # BERT is **not confident** in the original word
        and word_difference > 2  # Ensure significant difference (avoid synonyms)
        and top_suggestion.lower() != word.lower()  # Ignore minor variations
    ):
        return True

    return False  # If BERT is uncertain, do not flag as an error

# NOTE: Function for Suggestions
# Function to check for real-word spelling errors using BERT
def get_bert_suggestions(word, prev_word, next_word, full_text):

    if not prev_word or not next_word:
        return [], []  # Skip if no surrounding words
    
    # Use a longer context (3 words before and after)
    words = full_text.split()
    word_idx = words.index(word) if word in words else -1

    # Extract better context (e.g., "The bond sell rate increased")
    context_window = " ".join(words[max(0, word_idx - 3) : min(len(words), word_idx + 4)]).replace(word, "[MASK]")

    try:
        predictions = bert_corrector(context_window)
        bert_suggestions = [p['token_str'] for p in predictions[:3]]  # Top 3 predictions
        confidence_scores = [p['score'] for p in predictions[:3]]  # Corresponding confidence scores

        # Remove punctuation and symbols from suggestions
        bert_suggestions = [s for s in bert_suggestions if re.match(r"^[a-zA-Z'-]+$", s)]

        return bert_suggestions, confidence_scores
    except Exception as e:
        print(f"BERT Error: {e} | Word: '{word}'")
        return [], []

# Function to suggest corrections using SpellChecker + Bigram + BERT
def suggest_corrections(word, prev_word=None, next_word=None, full_text=None, top_n=5):

    word = word.lower().strip(".,!?")  # Normalize word for lookup
    
    # Get candidates from SpellChecker
    try:
        spell_candidates = spell.candidates(word)
        
        if spell_candidates is None:  # Handle None case explicitly
            spell_candidates = []

        spell_candidates = list(spell_candidates)  # Convert to list safely

    except Exception as e:
        print(f"Error: {e} | Problematic word: '{word}'")
        spell_candidates  = []  # Return an empty list instead of failing

    # Remove punctuation & symbols from spellchecker suggestions
    spell_candidates = [w for w in spell_candidates if re.match(r"^[a-zA-Z'-]+$", w)]

    # If there's a previous word, rank suggestions using bigram probabilities
    if prev_word or next_word:
        spell_candidates = sorted(
            spell_candidates ,
            key=lambda w: (
                distance(word, w),
                -word_freq.get(w, 0),  # Prioritize common words in Reuters
                -bigram_counts.get((prev_word, w), 0) if prev_word else 0,
                -bigram_counts.get((w, next_word), 0) if next_word else 0
                )
        )

    # Get **only highly relevant BERT-based corrections**
    if full_text is not None:
        bert_suggestions, _ = get_bert_suggestions(word, prev_word, next_word, full_text) if (prev_word or next_word) else []
    else:
        bert_suggestions = []

    # Merge SpellChecker + BERT suggestions **without duplicates**
    all_candidates = list(dict.fromkeys(spell_candidates + bert_suggestions))[:top_n]

    return all_candidates

# NOTE: Function for Detect + Suggestions
# Function to detect and suggest corrections in one step
def detect_and_suggest_corrections(text, top_n=5):

    # Extract original words as they appear in the input text
    words_original = re.findall(r"\b\w+['-]?\w*\b", text)
    
    # Normalize words to lowercase for SpellChecker lookup
    words_normalized = [word.lower().strip(".,!?") for word in words_original]

    misspelled_words = detect_misspellings(text)  # Detect non-word spelling errors
    corrections = {}

    print("Misspelled words detected by SpellChecker:")
    print(misspelled_words)

    for i, word in enumerate(words_original):
        normalized_word = words_normalized[i]  # Get the corresponding normalized word
        prev_word = words_original[i - 1] if i > 0 else None  # Get the previous word
        next_word = words_original[i + 1] if i < len(words_original) - 1 else None  # Get next word

        # Check for non-word spelling errors
        if word in misspelled_words:
            corrections[word] = suggest_corrections(normalized_word, prev_word, next_word)
        # Check for real-word spelling errors using BERT
        elif prev_word and next_word and is_real_word_error(prev_word, word, next_word, text):
            # Avoid duplicate detection
            if word not in corrections:
                misspelled_words.append(word) # Add to list of detected errors
                corrections[word] = suggest_corrections(normalized_word, prev_word, next_word, text, top_n)

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
    test_text = """
                The company announced an expantion into new international markets, aiming for increased revenue. 
                CEO mentioned that finacial resources are in place to support growth. 
                All departments have been informed accept logistics, which will receive updates soon. 
                Employees are excited about there new opportunities in global trade.
                """
    print(detect_and_suggest_corrections(test_text))
    pass