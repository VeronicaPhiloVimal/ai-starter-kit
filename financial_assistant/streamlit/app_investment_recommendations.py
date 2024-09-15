# financial_assistant/streamlit/app_investment_recommendations.py

import streamlit as st

def get_investment_recommendations():
    st.title("Investment Recommendations")

    # Check if the financial profile exists in session state
    if "financial_profile" not in st.session_state:
        st.warning("Please create your financial profile first.")
        return

    # Retrieve risk tolerance from the user's financial profile
    financial_profile = st.session_state["financial_profile"]
    risk_tolerance = financial_profile.get("risk_tolerance", "Medium")

    # Define recommendations based on risk tolerance
    recommendations = {
        "Low": ["Bonds", "Index Funds"],
        "Medium": ["Stocks", "ETFs"],
        "High": ["Cryptocurrency", "Growth Stocks"],
    }

    # Display recommendations based on risk tolerance
    st.write(f"Based on your risk tolerance ({risk_tolerance}), we recommend:")
    for investment in recommendations[risk_tolerance]:
        st.write(f"- {investment}")
