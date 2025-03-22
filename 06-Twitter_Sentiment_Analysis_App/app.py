import streamlit as st

# Load other apps
import eda_app
import ml_app
import info_app

# Create nav page
home_pg = st.Page(info_app.home_page, title='Home', icon='🏠')
eda_des_pg = st.Page(eda_app.eda_des_page, title='Summary Statistics', icon='📑')
eda_plot_pg = st.Page(eda_app.eda_plot_page, title='Data Visualizations', icon='📊')
ml_pg = st.Page(ml_app.ml_page, title='Twitter Tweets Sentiment Analysis', icon='💬')
about_pg = st.Page(info_app.about_page, title='About', icon='📖')

# Create navigation
nav = st.navigation({"Home": [home_pg], "Exploratory Data Analysis (EDA)": [eda_des_pg, eda_plot_pg], 
                     "Sentiment Analysis with ML": [ml_pg],"About": [about_pg]})
nav.run()