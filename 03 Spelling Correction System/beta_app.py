import streamlit as st
import time

def main_app():

    # NOTE: Spelling Error Tracker & Styling

    # Function to move between errors
    def move_error(direction):
        if direction == "next" and st.session_state["current_index"] < len(st.session_state["remaining_errors"]) - 1:
            st.session_state["current_index"] += 1
        elif direction == "previous" and st.session_state["current_index"] > 0:
            st.session_state["current_index"] -= 1
        
        st.rerun()

    # Function to replace the misspelled word with the selected suggestion
    def replace_word(selected_correction):
        if st.session_state["remaining_errors"]:
            current_word = st.session_state["remaining_errors"][st.session_state["current_index"]]
            
            # Replace in the corrected text
            st.session_state["corrected_text"] = st.session_state["corrected_text"].replace(current_word, selected_correction)

            # Remove the corrected word from the error list
            st.session_state["remaining_errors"].remove(current_word)

            # Adjust the index to prevent out-of-range errors
            if st.session_state["current_index"] >= len(st.session_state["remaining_errors"]):
                st.session_state["current_index"] = max(0, len(st.session_state["remaining_errors"]) - 1)

            st.rerun()

    # Function to highlight misspelled words dynamically
    def highlight_text(text, selected_word):
        for word in misspelled_words:
            if word in st.session_state["remaining_errors"]:
                if word == selected_word:
                    # Highlight the selected word in yellow
                    text = text.replace(word, f"<span class='misspelled selected'>{word}</span>")
                else:
                    # Other misspelled words remain bold + red underline
                    text = text.replace(word, f"<span class='misspelled'>{word}</span>")
        return text
    
    # Function to get the currently selected misspelled word & highlight text dynamically
    def get_highlight_word():
        # Get the currently selected misspelled word
        selected_word = (
            st.session_state["remaining_errors"][st.session_state["current_index"]]
            if st.session_state["remaining_errors"]
            else None
            )
        # Highlight text dynamically
        highlighted_text = highlight_text(st.session_state["corrected_text"], selected_word)
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
    st.title('Spelling Correction System 📝')

    # Description
    st.write("""This is a simple spelling correction system that is built using Financial Corpus. 
            You can input text or upload a file to check the spelling of the text.""")

    # NOTE: Dummy input and output

    # Input 
    input_text = """The qick brown fox jumpd over the lazi dog, whos tail was waggin happilly. He didn’t notic the brid flying abve, nor did he see the car approching fast. Evryone around was surprized by the scene, wondring how such an event cold happen so sudenly in broad daylight."""

    # Misspelled Words List
    misspelled_words = ["qick", "jumpd", "lazi", "whos", "waggin", "happilly", 
                        "notic", "brid", "abve", "approching",
                        "Evryone", "surprized", "wondring", "sudenly"]
    
    # Corrections Words List
    corrections = ["quick", "jumped", "lazy", ["who's", "whose"], "wagging", "happily",
                   "notice", ["bird", "birds"], "above", "approaching",
                   "Everyone", "surprised", "wondering", "suddenly"]

    # Corrections
    corrections_dict = dict(zip(misspelled_words, corrections))

    # NOTE: Session State

    # Function to initialize session state for spell check tracking
    def reset_spelling_state():
        st.session_state["current_index"] = 0 # Track which misspelled words is selected
        st.session_state["corrected_text"] = input_text # Stores updated text
        st.session_state["remaining_errors"] = misspelled_words.copy() # Track remaining errors

    # Ensure Spelling Check session state variables exist
    if "corrected_text" not in st.session_state:
        reset_spelling_state()
    
    # Ensure analyze click state exists 
    if "analyze_clicked" not in st.session_state:
        st.session_state["analyze_clicked"] = False

    # Ensure expander open state exists
    if "expander_open" not in st.session_state:
        st.session_state["expander_open"] = False

    # Ensure last input choice state exists
    if "last_input_choice" not in st.session_state:
        st.session_state["last_input_choice"] = None

    # Ensure loading session state exists
    if "loading" not in st.session_state:
        st.session_state["loading"] = False

    # NOTE: Input Section

    # Subheader
    st.subheader("Input 📥")

    with st.expander("Click here to choose the input method"):
        input_type = ['Text', 'File Upload']
        input_choice = st.radio('Select Input Type', input_type)

        # Detect if the user switched input methods
        if input_choice != st.session_state["last_input_choice"]:
            st.session_state["last_input_choice"] = input_choice
            reset_spelling_state()
            st.session_state["analyze_clicked"] = False
            st.session_state["expander_open"] = False

        if input_choice == 'Text':
            # Text Input
            text_input = st.text_area('Enter Text:', height=200, max_chars=500, value=input_text)

        elif input_choice == 'File Upload':
            # File Upload
            file = st.file_uploader('Upload File:', type=['txt', 'csv', 'pdf', 'docx'])
            file_text = "Text from uploaded file."

    # Create column for "Analyze Text" and "Reset Text" buttons
    col1, col2, col3  = st.columns([1.1, 1, 4])

    with col1:
        # Click button and display output as expander
        if st.button("Analyze Text"):

            # Start loading
            st.session_state["loading"] = True
            
            # Mark that analyze button was clicked
            st.session_state["analyze_clicked"] = True
            st.session_state["expander_open"] = False

            # Reset spelling state to initial state on each analysis
            reset_spelling_state()

    if st.session_state["loading"]:
        # Add spinner
        with st.spinner("Checking for spelling errors...", show_time=True):
            time.sleep(2)
            st.toast("Spelling Check Done!", icon="✅")

        # Stop loading after the process completes
        st.session_state["loading"] = False

    with col2:
        # Reset button
        if st.button("Reset"):
            st.session_state["analyze_clicked"] = False
            st.session_state["expander_open"] = False
            reset_spelling_state()
        

    # NOTE: Text Analysis

    # Only show the spelling check results if the "Analyze Text" button was clicked
    if st.session_state["analyze_clicked"]:

        st.subheader("Spelling Check 🔍")

        with st.expander("Click here to view the spelling check results", expanded=st.session_state["expander_open"]):
            
            # Keep the expander open once it open
            st.session_state["expander_open"] = True

            # Display the number of misspelled words
            if len(st.session_state['remaining_errors']) > 0 and input_choice == "Text":

                selected_word = get_highlight_word()

                st.error(f"Number of Misspelled Words: {len(st.session_state['remaining_errors'])}")

                st.write()

                # Create three columns
                col1, col2, col3 = st.columns([3, 0.6, 0.5])

                with col1:
                    suggestion_container = st.container(border=True)

                    with suggestion_container:
                        st.markdown("#### Suggested Corrections 📌")
                        st.write(f"**Misspelled Word:** {selected_word}")
                        selected_correction = st.radio("Select a correction:", corrections_dict[selected_word])

                        # Replace button
                        if st.button("Replace"):
                            replace_word(selected_correction)
                
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
                
                if input_choice == "Text":
                    # Get corrected text
                    corrected_text = st.session_state["corrected_text"]
                else:
                    corrected_text = file_text

                st.markdown(f'<div class="bordered-box">{corrected_text}</div>', unsafe_allow_html=True)

                st.success("No spelling errors found!")

                # Download Text
                st.download_button("Download Corrected Text (txt)", corrected_text, "corrected_text.txt")

def about_app():
    st.title("About 📖")
    st.write("""
    This is a simple spelling correction system that is built using Financial Corpus. 
    You can input text or upload a file to check the spelling of the text.
    """)

    st.subheader("Team members 👨‍💻")
    st.write("[Member 1]")
    st.write("[Member 2]")
    st.write("[Member 3]")

    st.subheader("Data Source 🛢️")
    st.write("""
    The Financial Corpus is a collection of financial news articles from various sources. Link
    to the dataset: [Financial News Dataset](https://www.kaggle.com/jeet2016/us-financial-news-articles)
    """)

    st.subheader("About the Data")
    st.write("[Insert Graphs]")

    st.subheader("Methodology 🛠️")
    st.write("1️⃣ Step 1")
    st.write("2️⃣ Step 2")
    st.write("3️⃣ Step 3")
    st.write("4️⃣ Step 4")
    st.write("5️⃣ Step 5")

    st.subheader("Model Performance 📊")
    st.write("[Insert Graphs and Tables]")

    st.subheader("Future Work 🚀")
    st.write("1️⃣ Recommendations 1")
    st.write("2️⃣ Recommendations 2")
    st.write("3️⃣ Recommendations 3")

# Create Page
main_pg = st.Page(main_app, title="Spelling Correction System", icon="📝")
about_pg = st.Page(about_app, title="About", icon="📖")

# Create Navigation
nav = st.navigation([main_pg, about_pg])
nav.run()