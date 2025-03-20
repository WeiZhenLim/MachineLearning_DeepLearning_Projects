import streamlit as st

# Load ML Packages
import joblib
import os

# Load utils
from utils import show_banner

def ml_page():
    show_banner()
    st.title("Diabetes Prediction with ML 🩺")
