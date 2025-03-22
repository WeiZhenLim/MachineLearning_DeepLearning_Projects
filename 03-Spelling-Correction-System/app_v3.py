import streamlit as st
import time
import re

from spelling_sys.SpellCheckerHybridNGram_v3 import detect_and_suggest_corrections, plot_doc_cat_dis, plot_doc_length_hist, plot_top_n_most_frequent_words, plot_word_cloud

def main_app():

    # NOTE: Spelling Error Tracker & Styling

    # Function to move between errors
    def move_error(direction):
        if direction == "next":
            # If at the last word, loop back to the first one
            if st.session_state["current_index"] >= len(st.session_state["remaining_errors"]) - 1:
                st.session_state["current_index"] = 0  # Loop back to first misspelled word
            else:
                st.session_state["current_index"] += 1

        elif direction == "previous":
            # If at the first word, loop back to the last one
            if st.session_state["current_index"] <= 0:
                st.session_state["current_index"] = len(st.session_state["remaining_errors"]) - 1  # Loop back to last misspelled word
            else:
                st.session_state["current_index"] -= 1

        st.rerun()

    # Function to replace the misspelled word with the selected suggestion
    def replace_word(selected_correction):
        if st.session_state["remaining_errors"]:
            current_word = st.session_state["remaining_errors"][st.session_state["current_index"]]
            
            # Use regex to find and replace the misspelled word while keeping punctuation
            pattern = rf'\b{re.escape(current_word)}(\W*)'  # Matches word + optional punctuation
            st.session_state["corrected_text"] = re.sub(
                pattern, 
                lambda m: selected_correction + m.group(1),  # Retains punctuation
                st.session_state["corrected_text"]
            )
            
            # Remove the corrected word from the error list
            st.session_state["remaining_errors"].remove(current_word)

            # Adjust the index to prevent out-of-range errors
            if st.session_state["current_index"] >= len(st.session_state["remaining_errors"]):
                st.session_state["current_index"] = max(0, len(st.session_state["remaining_errors"]) - 1)

            st.rerun()

    # Function to highlight misspelled words dynamically
    def highlight_text(text, selected_word, misspelled_words):
        def replacement(match):
            word = match.group(0)  # Extract matched word
            if word == selected_word:
                return f"<span class='misspelled selected'>{word}</span>"
            else:
                return f"<span class='misspelled'>{word}</span>"

        # Ensure the regex properly matches the last word without space issues
        pattern = r'\b(' + '|'.join(re.escape(word) for word in misspelled_words) + r')(?!\w)'
        text = re.sub(pattern, replacement, text)

        return text
        
    # Function to get the currently selected misspelled word & highlight text dynamically
    def get_highlight_word(misspelled_words):
        # Get the currently selected misspelled word
        selected_word = (
            st.session_state["remaining_errors"][st.session_state["current_index"]]
            if st.session_state["remaining_errors"]
            else None
            )
        # Highlight text dynamically
        highlighted_text = highlight_text(st.session_state["corrected_text"], selected_word, misspelled_words)
        st.markdown(f"""<div class="bordered-box">{highlighted_text}</div>""", unsafe_allow_html=True)

        return selected_word

    # Custom CSS for highlighting words
    st.markdown(
        """
        <style>
        .misspelled {
            text-decoration: underline;
            text-decoration-color: red;
            text-decoration-style: wavy;
            font-weight: bold;
        }
        .selected {
            background-color: yellow;
            font-weight: bold;
            padding: 2px;
            border-radius: 3px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Custom CSS for border
    st.markdown(
    """
    <style>
    .bordered-box {
        border: 2px solid #bbbbbb; /* Green border */
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True  
    )

    # NOTE: Start of the App

    # Title
    st.title('📰 Business & Finance Spell Checker (Reuters-Based)')

    # Description
    st.write("""This is a simple spelling correction system that is built using Reuters Corpus. 
            You can input text (500 characters) to check the spelling of the text.""")

    # NOTE: Session State

    # Function to initialize session state for spell check tracking
    def reset_spelling_state(text_input, misspelled_words=None):
        st.session_state["current_index"] = 0 # Track which misspelled words is selected
        st.session_state["corrected_text"] = text_input # Stores updated text
        
        if misspelled_words is not None:
            st.session_state["remaining_errors"] = misspelled_words.copy() # Track remaining errors

    # Ensure Spelling Check session state variables exist
    if "corrected_text" not in st.session_state:
        reset_spelling_state("")
    
    # Ensure analyze click state exists 
    if "analyze_clicked" not in st.session_state:
        st.session_state["analyze_clicked"] = False

    # Ensure expander open state exists
    if "expander_open" not in st.session_state:
        st.session_state["expander_open"] = False

    # Ensure last input choice state exists
    if "last_input_choice" not in st.session_state:
        st.session_state["last_input_choice"] = None

    # Ensure session state exists for input fields
    if "text_input" not in st.session_state:
        st.session_state["text_input"] = ""

    if "file_upload" not in st.session_state:
        st.session_state["file_upload"] = None

    # Ensure loading session state exists
    if "loading" not in st.session_state:
        st.session_state["loading"] = False

    # NOTE: Input Section

    # Subheader
    st.subheader("Input 📥")

    # Text Input
    with st.container(border=True):
        text_input = st.text_area('Enter Text:', height=200, max_chars=500, value=st.session_state["text_input"])

    # Update session state
    st.session_state["text_input"] = text_input

    # Create column for "Analyze Text" and "Reset Text" buttons
    col1, col2, col3  = st.columns([1.1, 1, 4])

    with col1:
        # Click button and display output as expander
        if st.button("Analyze Text"):
            
            # NOTE: Text Analysis
            misspelled_words, corrections_dict = detect_and_suggest_corrections(text_input)

            # Store results in session state
            st.session_state["misspelled_words"] = misspelled_words
            st.session_state["corrections_dict"] = corrections_dict

            # Start loading
            st.session_state["loading"] = True
            
            # Mark that analyze button was clicked
            st.session_state["analyze_clicked"] = True
            st.session_state["expander_open"] = False

            # Reset spelling state to initial state on each analysis
            reset_spelling_state(text_input, misspelled_words)

    if st.session_state["loading"]:
        # Add spinner
        with st.spinner("Checking for spelling errors...", show_time=True):
            time.sleep(1)
            st.toast("Spelling Check Done!", icon="✅")

        # Stop loading after the process completes
        st.session_state["loading"] = False

    with col2:
        # Reset button
        if st.button("Reset"):
            st.session_state["analyze_clicked"] = False
            st.session_state["expander_open"] = False
            st.session_state["text_input"] = ""

            st.rerun()

    if st.session_state["analyze_clicked"] and len(text_input) == 0:
        st.error("⚠️ Please enter some text for the spell check.")

    # NOTE: Display Analysis Results

    # Only show the spelling check results if the "Analyze Text" button was clicked
    if st.session_state["analyze_clicked"] and len(text_input) > 0:

        st.subheader("Spelling Check 🔍")

        with st.expander("Click here to view the spelling check results", expanded=st.session_state["expander_open"]):
            
            # Keep the expander open once it open
            st.session_state["expander_open"] = True

            # Display the number of misspelled words
            if len(st.session_state['remaining_errors']) > 0:
                
                selected_word = get_highlight_word(st.session_state["misspelled_words"])

                st.error(f"Number of Misspelled Words: {len(st.session_state['remaining_errors'])}")

                st.write()

                # Create three columns
                col1, col2, col3 = st.columns([3, 0.6, 0.5])

                with col1:
                    suggestion_container = st.container(border=True)

                    with suggestion_container:
                        st.markdown("#### Suggested Corrections 📌")
                        st.write(f"**Misspelled Word:** {selected_word}")
                        selected_correction = st.radio("Select a correction:", st.session_state["corrections_dict"][selected_word])

                        # Replace button
                        if st.button("Replace"):
                            replace_word(selected_correction)

                            # NOTE: Rerun Text Analysis Again (Taking correlation between words into consideration)
                            misspelled_words, corrections_dict = detect_and_suggest_corrections(st.session_state["corrected_text"])

                            # Store results in session state
                            st.session_state["misspelled_words"] = misspelled_words
                            st.session_state["corrections_dict"] = corrections_dict
                
                with col2:
                    if st.button("Previous") and selected_word:
                        move_error("previous")

                with col3:
                    if st.button("Next") and selected_word:
                        move_error("next")

                # Get corrected text
                corrected_text = st.session_state["corrected_text"]

                # Download Text
                st.download_button("Download Partially Corrected Text (txt)", corrected_text, "corrected_text.txt")

                # Display warning message
                st.warning("There are spelling errors in the text. You can still download it, ignoring the errors.")

            else:
                
                # Get corrected text
                corrected_text = st.session_state["corrected_text"]

                st.markdown(f'<div class="bordered-box">{corrected_text}</div>', unsafe_allow_html=True)

                st.success("No spelling errors found!")

                # Download Text
                st.download_button("Download Corrected Text (txt)", corrected_text, "corrected_text.txt")

def about_app():
    st.title("About 📖")
    st.write("""
    This is a simple spelling correction system that is built using Reuters Corpus. 
    You can input text or upload a file to check the spelling of the text.
    """)

    st.subheader("Team members 👨‍💻")
    st.write("Lim Wei Zhen")
    st.write("Chia Zhi Xuan")
    st.write("Chow Mei Foong")

    st.subheader("Data Source 🛢️")
    st.write("""
    The Reuters Corpus is a large collection of Reuters News stories for use in research and development of 
    natural language processing, information retrieval, and machine learning systems. Link
    to the dataset: [Reuters Corpus](https://trec.nist.gov/data/reuters/reuters.html)
    """)

    st.subheader("About the Data")
    st.write()
    with st.expander("Word Frequency Distribution"):
        plt = plot_top_n_most_frequent_words(20, (15,6))
        st.pyplot(plt)

    with st.expander("Word Cloud"):
        plt = plot_word_cloud(500, 150, (10, 5))
        st.pyplot(plt)

    with st.expander("Document Categories Distribution"):
        plt = plot_doc_cat_dis(5, (7, 7))
        st.pyplot(plt)

    with st.expander("Document Length Distribution"):
        plt = plot_doc_length_hist((15, 6), 50)
        st.pyplot(plt)

    st.subheader("Methodology 🛠️")
    st.write("This spelling correction system leverages natural language processing (NLP) techniques and statistical language models to detect and correct misspelled words.")
    st.write("""
             📌 **Data Source & Preprocessing**
            - Corpus: Utilizes the Reuters corpus from NLTK as a reference dataset.
            - Preprocessing:
              - Converts text to lowercase.
              - Tokenizes words and removes punctuation.
              - Eliminates stopwords to reduce noise.
              - Filters out words that are not in the English dictionary.
              - Applies lemmatization to standardize words.
            """)
    st.write("""
             📌 **Language Models for Context-Aware Spelling Correction**
            - Bigram & Trigram Models:
              - Builds bigram (two-word sequences) and trigram (three-word sequences) models from the Reuters dataset.
              - Uses Laplace Smoothing to handle unseen word combinations.
              - Calculates bigram & trigram probabilities to assess word correctness in context.
            """)
    st.write("""
             📌 **Spelling Error Detection & Correction**
            - Misspelled Words Detection:
              - Uses PySpellChecker to identify words that do not exist in the Reuters vocabulary.
              - Preserves original word formatting for better readability.
            - Correction Suggestion:
              - Generates possible corrections using edit distance and word frequency.
              - Ranks corrections based on:
                - Word frequency in Reuters corpus.
                - Bigram & trigram probabilities to ensure contextual relevance.
            """)

    st.subheader("Future Work 🚀")
    st.write("1️⃣ Enhancing Real-Word Error Detection – The current system struggles with real-word spelling errors (e.g., sell vs. cell). Future improvements may integrate semantic models like Word2Vec or contextual embeddings to better understand word usage.")
    st.write("2️⃣ Expanding Training Data – Incorporating a larger and more diverse dataset beyond the Reuters corpus, such as general news articles or Wikipedia, to improve language coverage and adaptability.")
    st.write("3️⃣ Grammar & Sentence Structure Analysis – Introducing grammatical error detection alongside spelling correction to improve overall text coherence and correctness.")

# Create Page
main_pg = st.Page(main_app, title="Spelling Correction System", icon="📝")
about_pg = st.Page(about_app, title="About", icon="📖")

# Create Navigation
nav = st.navigation([main_pg, about_pg])
nav.run()