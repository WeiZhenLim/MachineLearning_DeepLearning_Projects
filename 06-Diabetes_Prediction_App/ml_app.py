import streamlit as st

# Load ML Packages
import joblib
import os

# Load EDA Packages
import numpy as np
import pandas as pd

# Load utils
from utils import show_banner, expander_formatter

attribute_info = """
1. Age: 1.20-65		
1. Sex: 1. Male, 2.Female		
1. Polyuria: 1.Yes, 2.No.		
1. Polydipsia: 1.Yes, 2.No.		
1. sudden weight loss: 1.Yes, 2.No.		
1. weakness: 1.Yes, 2.No.		
1. Polyphagia: 1.Yes, 2.No.		
1. Genital thrush: 1.Yes, 2.No.		
1. visual blurring: 1.Yes, 2.No.		
1. Itching: 1.Yes, 2.No.		
1. Irritability: 1.Yes, 2.No.		
1. delayed healing: 1.Yes, 2.No.		
1. partial paresis: 1.Yes, 2.No.		
1. muscle stiffness: 1.Yes, 2.No.		
1. Alopecia: 1.Yes, 2.No.		
1. Obesity: 1.Yes, 2.No.		
1. Class: 1.Positive, 2.Negative.		
"""

label_dict = {"No":0, "Yes":1}
gender_map = {"Female":0, "Male":1}
target_label_map = {"Negative":0, "Positive":1}

# NOTE: Function for input conversion
def get_fvalue(val):
    feature_dict = {"No":0, "Yes":1}

    for key, value in feature_dict.items():
        if val == key:
            return value
        
def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value

# NOTE: Function to Lead ML MOdels
@st.cache_resource
def load_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file), "rb"))
    return loaded_model

# NOTE: ML Page
def ml_page():
    show_banner()
    st.title("Diabetes Prediction with ML 🩺")

    expander_formatter(16)

    with st.expander("Attribute Information"):
        st.write(attribute_info)

    # Input
    with st.form(key='att_input'):
        
        st.write("#### Attribute Input for Diabetes Prediction")

        # Layout
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age (10 - 100)", 10, 100, 25)
            gender = st.radio("Gender", ["Female", "Male"], horizontal=True)
            polyuria = st.radio("Polyuria", ["No", "Yes"], horizontal=True)
            polydipsia = st.radio("Polydipsia", ["No", "Yes"], horizontal=True)
            sudden_weight_loss = st.radio("Sudden Weight Loss", ["No", "Yes"], horizontal=True)
            weakness = st.radio("Weakness", ["No", "Yes"], horizontal=True)
            polyphagia = st.radio("Polyphagia", ["No", "Yes"], horizontal=True)
            genital_thrush = st.radio("Genital Thrush", ["No", "Yes"], horizontal=True)
            

        with col2:
            visual_blurring = st.radio("Visual Blurring", ["No", "Yes"], horizontal=True)
            itching = st.radio("Itching", ["No", "Yes"], horizontal=True)
            irritability = st.radio("Irritability", ["No", "Yes"], horizontal=True)
            delayed_healing = st.radio("Delayed Healing", ["No", "Yes"], horizontal=True)
            partial_paresis = st.radio("Partial Paresis", ["No", "Yes"], horizontal=True)
            muscle_stiffness = st.radio("Muscle Stiffness", ["No", "Yes"], horizontal=True)
            alopecia = st.radio("Alopecia", ["No", "Yes"], horizontal=True)
            obesity = st.radio("Obesity", ["No", "Yes"], horizontal=True)

        submit_info = st.form_submit_button(label="Predict")

    # Actions After Clicking Submit Button
    if submit_info:
        # Display Submitted Input
        with st.expander("Submitted Input"):
            result = {
                'age': age,
                'gender': gender,
                'polyuria': polyuria,
                'polydipsia': polydipsia,
                'sudden_weight_loss': sudden_weight_loss,
                'weakness': weakness,
                'polyphagia': polyphagia,
                'genital_thrush': genital_thrush,
                'visual_blurring': visual_blurring,
                'itching': itching,
                'irritability': irritability,
                'delayed_healing': delayed_healing,
                'partial_paresis': partial_paresis,
                'muscle_stiffness': muscle_stiffness,
                'alopecia': alopecia,
                'obesity': obesity
            }

            df_result = pd.DataFrame([result]).T
            df_result.columns = ["Submitted Values"]

            st.dataframe(df_result, use_container_width=True)

            encoded_result = []
            for i in result.values():
                if type(i) == int:
                    encoded_result.append(i)
                elif i in ["Female", "Male"]:
                    res = get_value(i, gender_map)
                    encoded_result.append(res)
                else:
                    encoded_result.append(get_fvalue(i))

        # Prediction Result
        with st.expander("Prediction Result"):
            single_sample = np.array(encoded_result).reshape(1, -1)

            model = load_model("models/logistic_regression_model_diabetes.pkl")
            prediction = model.predict(single_sample)
            pred_prob = model.predict_proba(single_sample)

            pred_probability_score = {"Negative Diabetes Risk": str(round(pred_prob[0][0]*100,2)) + "%", "Positive Diabetes Risk": str(round(pred_prob[0][1]*100,2)) + "%"}
            score_df = pd.DataFrame([pred_probability_score]).T
            score_df.columns = ["Probability"]
            
            if prediction == 1:
                st.warning("⚠️ Your results indicate a **high risk of diabetes**")
                st.dataframe(score_df, use_container_width=True)
            else:
                st.success("✅ Your results indicate a **low risk of diabetes**")
                st.dataframe(score_df, use_container_width=True)