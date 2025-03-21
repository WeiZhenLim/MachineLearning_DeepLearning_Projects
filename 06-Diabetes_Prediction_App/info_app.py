import streamlit as st

# Load utils
from utils import show_banner

def home_page():
    show_banner()
    st.title("Home 🏠")

    st.subheader("Early Stage Diabetes Risk Predictor App")
    st.write("""
             This app predicts the risk of developing early-stage diabetes using ML models trained on a dataset
             containing signs and symptoms of newly diagnosed or at-risk diabetic patients.
             """)

    st.subheader("Data Source")
    st.write("Early Stage Diabetes Risk Prediction Dataset from UCI Machine Learning Repository")
    st.write("🔗[**Link to Data Source**](https://archive.ics.uci.edu/dataset/529/early+stage+diabetes+risk+prediction+dataset)")

    st.subheader("App Content")
    st.write("This app contains multiple sections to guide users through the diabetes prediction process:")
    st.write("1️⃣ **Home:** Provides an overview of the application and its purpose.")
    st.write("2️⃣ **Exploratory Data Analysis (EDA):** Visualizes and explores key trends in the dataset.")
    st.write("3️⃣ **Diabetes Prediction (ML):** Uses machine learning models to predict diabetes risk based on input data.")
    st.write("4️⃣ **About:** Offers information about the dataset, methodology, and application development.")

def about_page():
    show_banner()
    st.title("About Diabetes Prediction App 📖")

    st.markdown(
        """
        ## 📌 About This App
        This application is a **Diabetes Prediction Tool** built using **Streamlit**. It allows users to assess their risk of developing **early-stage diabetes** using **Machine Learning (ML) models** trained on medical data.  

        The app analyzes user-provided health information and predicts whether the individual has a **high or low risk of diabetes** based on their symptoms and risk factors.
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🔧 Technologies Used")
    st.write("- **Streamlit** for UI and app deployment")
    st.write("- **Scikit-learn** for machine learning model training and inference")
    st.write("- **Pandas & NumPy** for data processing")
    st.write("- **Matplotlib & Seaborn** for data visualization")
    st.write("- **Plotly** for interactive charts")

    st.markdown("## 🎯 Features")
    st.write(
        """
        - **Predict diabetes risk** based on user inputs
        - **Perform exploratory data analysis (EDA)** to understand trends in diabetes-related data
        - **Interactive visualizations** for data insights
        - **User-friendly interface** with real-time processing
        """
    )

    st.markdown("## 👨‍💻 Developer")
    st.write("**Developed by: Lim Wei Zhen**")
    st.write("**GitHub:** [Link](https://github.com/WeiZhenLim)")
    st.write("**LinkedIn:** [Link](https://www.linkedin.com/in/weizhen-lim/)")

    st.markdown("## 📚 Learning Resources")
    st.write(
        """
        This project was built using knowledge gained from the Udemy course:  
        **[Streamlit for Data Science and Machine Learning](https://www.udemy.com/share/103Mg23@lrrcYB5c9ZvznO0Oc6LD691ZFuIsmh_HumMlHZcZ6GyBZXxSC7va-YKFuym8XZWi2g==/)**  
        """
    )
    st.write("**Instructor:** Jesse E. Agbe [(Link to Bio)](https://www.udemy.com/user/jesse-e-agbe/)")

    st.markdown("## 💡 How to Use?")
    st.write("1️⃣ Enter relevant health information into the form on the main page.")
    st.write("2️⃣ Click **Predict** to get the diabetes risk assessment.")
    st.write("3️⃣ View the **prediction result** and additional insights.")
    st.write("4️⃣ Click **Reset** to clear the inputs and start over.")

    st.info("""📢 This project is a demonstration of machine learning for diabetes prediction. 
            It is not a medical diagnosis tool. 
            Always consult a healthcare professional for accurate medical assessments.""")