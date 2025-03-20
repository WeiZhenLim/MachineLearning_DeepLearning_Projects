import streamlit as st

# Load EDA Packages
import pandas as pd

# Load Data Viz Packages
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import plotly.express as px

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

    st.subheader("Descriptive Analysis 📑")
    st.write("This section provides a descriptive analysis of the Early Stage Diabetes Risk Prediction dataset.")

    # Load dataset
    df = load_data("data/diabetes_data_upload.csv")
    df_encoded = load_data("data/diabetes_data_upload_clean.csv")

    # Format expander font size
    expander_formatter(16)

    with st.expander("Overview of Raw Data"):       
        st.dataframe(df, height=250)

    with st.expander("Data Types"):
        # Create dataframe for dtypes
        df_types = df.dtypes.reset_index()
        df_types.columns = ["Column Name", "Data Type"]
        st.dataframe(df_types, use_container_width=True)

    with st.expander("Descriptive Summary"): 
        st.dataframe(df_encoded.describe(), use_container_width=True)

    with st.expander("Class Distribution"):
        st.dataframe(df['class'].value_counts(), use_container_width=True)

    with st.expander("Gender Distribution"):
        st.dataframe(df['Gender'].value_counts(), use_container_width=True)

def eda_plot_page():
    show_banner()
    st.title("Exploratory Data Analysis 🔍")

    st.subheader("Data Visualization 📊")
    st.write("This section provides various data visualization plots to help understand the Early Stage Diabetes Risk Prediction dataset.")