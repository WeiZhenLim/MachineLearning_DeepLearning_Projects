import streamlit as st

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

    # NOTE: Define session state
    # Initialize a session state
    if "analyze_clicked" not in st.session_state:
        st.session_state["analyze_clicked"] = False

    # NOTE: Input
    # Text Area Input for User
    st.markdown("#### Input 📥")

    with st.container(border=True):
        
        text = st.text_area("Enter Text:")
        st.session_state["analyze_clicked"] = st.button("Analyze Text")

    # NOTE: Analysis Results
    # Output for User (Only show after user click on Analyze Text)
    if st.session_state["analyze_clicked"]:
        st.markdown("#### Analysis Results 📤")

        # Create two columns for the analysis results
        col1, col2 = st.columns([2.5, 1.5])

        # Show the polarity & subjectivity, sentiment score, and graphs
        with col1:
            
            with st.expander("Results Breakdown"):
                st.write("Results")

            pass

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