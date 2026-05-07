import streamlit as st
import pickle
import numpy as np


def show():
    st.title("📊 Diabetes Prediction AI")

    # ✅ Load model inside show() to avoid module-level errors
    try:
        model = pickle.load(open("diabetes_model.pkl", "rb"))
    except Exception as e:
        st.error(f"❌ Error loading diabetes model: {e}")
        st.stop()

    preg    = st.number_input("Pregnancies",     min_value=0)
    glucose = st.number_input("Glucose Level",   min_value=0)
    bp      = st.number_input("Blood Pressure",  min_value=0)
    skin    = st.number_input("Skin Thickness",  min_value=0)
    insulin = st.number_input("Insulin",         min_value=0)
    bmi     = st.number_input("BMI",             min_value=0.0, format="%.1f")
    age     = st.number_input("Age",             min_value=0)

    if st.button("Predict"):
        data = np.array([[preg, glucose, bp, skin, insulin, bmi, age]])
        prediction = model.predict(data)

        if prediction[0] == 1:
            st.error("⚠️ The person is Diabetic")
        else:
            st.success("✅ The person is Not Diabetic")

    st.write("⚠️ For education only. Consult a doctor.")
