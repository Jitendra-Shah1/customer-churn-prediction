import streamlit as st
import requests
url='http://backend:8000/predict'


st.title("Customer Churn Prediction")

# Collecting user input
credit_score = st.number_input("Credit Score", min_value=0)
geography = st.selectbox("Geography", ["France", "Spain", "Germany"])
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=18)
balance = st.number_input("Balance", min_value=0.0)
tenure = st.number_input("Tenure", min_value=0)
num_products = st.number_input("Num Of Products", min_value=1)
has_card = st.selectbox("Has Credit Card", [0, 1])
is_active = st.selectbox("Is Active Member", [0, 1])
salary = st.number_input("Estimated Salary", min_value=0.0)

if st.button("Predict"):
    payload = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Balance": balance,
        "Tenure": tenure,
        "NumOfProducts": num_products,
        "HasCrCard": has_card,
        "IsActiveMember": is_active,
        "EstimatedSalary": salary
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        output=result['response']
        st.write(f"Prediction: {output['prediction']}")
        st.write(f"Probability: {output['probability']:.2f}")
    else:
        st.error("Error calling API")
