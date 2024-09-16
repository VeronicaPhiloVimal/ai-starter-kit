# financial_assistant/streamlit/app_ai_report.py

import streamlit as st
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_ai_report():
    logger.info("Generating AI report...")

    try:
        # Fetch the most recent data from session state or other sources
        user_profile = st.session_state.get('user_profile', 'No user profile data available')
        market_insights = st.session_state.get('market_insights', 'No market insights data available')

        # Generate report content based on the retrieved data
        report_content = "Generated AI Report based on the available data:\n"
        report_content += f"User Profile: {user_profile}\n"
        report_content += f"Market Insights: {market_insights}\n"

        # Display the generated report
        st.write(report_content)

    except Exception as e:
        logger.error(f"An error occurred while generating the AI report: {e}")
        st.error(f"An error occurred while generating the AI report: {e}")
