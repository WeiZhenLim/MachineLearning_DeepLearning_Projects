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

url_data = "https://raw.githubusercontent.com/WeiZhenLim/MachineLearning_DeepLearning_Projects/main/05-Diabetes_Prediction_App/data/diabetes_data_upload.csv"
url_clean_data = "https://raw.githubusercontent.com/WeiZhenLim/MachineLearning_DeepLearning_Projects/main/05-Diabetes_Prediction_App/data/diabetes_data_upload_clean.csv"
url_freq_data = "https://raw.githubusercontent.com/WeiZhenLim/MachineLearning_DeepLearning_Projects/main/05-Diabetes_Prediction_App/data/freqdist_of_age_data.csv"

# NOTE: Apps
def eda_des_page():
    show_banner()
    st.title("Exploratory Data Analysis 🔍")

    st.subheader("Descriptive Analysis 📑")
    st.write("This section provides a descriptive analysis of the Early Stage Diabetes Risk Prediction dataset.")

    # Load dataset
    df = load_data(url_data)
    df_encoded = load_data(url_clean_data)

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

    # Load dataset
    df = load_data(url_data)
    df_encoded = load_data(url_clean_data)
    df_freq = load_data(url_freq_data)[['Age', 'count']]

    # Format expander font size
    expander_formatter(16)

    # Layouts for Gender Distribution
    col1, col2 = st.columns([2,1])

    with col1:

        with st.expander("Dist Plot of Gender"):

            gen_df = df["Gender"].value_counts().reset_index()
            gen_df.columns = ["Gender", "Count"]

            p1 = px.pie(gen_df, names='Gender', values='Count', color_discrete_sequence=px.colors.qualitative.D3)
            st.plotly_chart(p1, use_container_width=True)

    with col2:
        with st.expander("Gender Distribution"):
            st.dataframe(gen_df, hide_index=True, use_container_width=True)

    # Layouts for Class Distribution
    col3, col4 = st.columns([2,1])

    with col3:

        with st.expander("Dist Plot of Class"):

            class_df = df["class"].value_counts().reset_index()
            class_df.columns = ["Class", "Count"]

            p2 = px.bar(class_df, x='Class', y='Count', color='Class', color_discrete_sequence=px.colors.qualitative.D3)
            st.plotly_chart(p2, use_container_width=True)

    with col4:

        with st.expander("Class Distribution"):
            st.dataframe(class_df, hide_index=True, use_container_width=True)

    # Freq Dist
    with st.expander("Frequency Distribution of Age"):

        p3 = px.bar(df_freq, x='Age', y='count', color_discrete_sequence=px.colors.qualitative.D3)
        st.plotly_chart(p3, use_container_width=True)

    # Outlier Detection
    with st.expander("Outlier Detection Plot"):

        p4 = px.box(df, x='Age', color='Gender', color_discrete_sequence=px.colors.qualitative.D3)
        st.plotly_chart(p4, use_container_width=True)

    # Correlation 
    with st.expander("Correlation Matrix"):
        corr_matrix = df_encoded.corr()

        p5 = px.imshow(corr_matrix, color_continuous_scale="Plasma")
        st.plotly_chart(p5, use_container_width=True)