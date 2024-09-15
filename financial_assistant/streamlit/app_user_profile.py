# financial_assistant/streamlit/app_user_profile.py

import streamlit as st

def generate_user_profile():
    st.title("User Financial Profile Generation")

    # Example fields for financial profile creation
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=18, max_value=100, value=25)
    income = st.number_input("Enter your annual income ($)", min_value=0)
    risk_tolerance = st.selectbox("Select your risk tolerance", ["Low", "Medium", "High"])

    # Store the financial profile in session state
    if st.button("Generate Profile"):
        st.session_state["financial_profile"] = {
            "name": name,
            "age": age,
            "income": income,
            "risk_tolerance": risk_tolerance
        }
        st.success("Financial profile generated successfully!")
