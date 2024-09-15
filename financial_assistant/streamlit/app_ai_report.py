# financial_assistant/streamlit/app_ai_report.py

import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_ai_report():
    st.title("Generative AI Report")

    # Check if chat history or data exists to generate a report
    if "chat_history" not in st.session_state or not st.session_state["chat_history"]:
        st.warning("No data available to generate the report. Please start a session.")
        return
    
    if "financial_profile" not in st.session_state:
        st.warning("Please complete your financial profile before generating the report.")
        return
    if "stock_analysis" not in st.session_state:
        st.warning("Please complete stock analysis before generating the report.")
        return

    # Create a buffer to store the PDF
    buffer = BytesIO()

    # Create PDF canvas and setup
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Financial Insights Report")

    # Add title to the PDF
    pdf.setFont("Helvetica", 18)
    pdf.drawString(100, 750, "Financial Insights Report")

    # Add chat history to the report
    pdf.setFont("Helvetica", 12)
    y_position = 700
    for index, entry in enumerate(st.session_state["chat_history"]):
        pdf.drawString(100, y_position, f"{index + 1}. {entry}")
        y_position -= 20
        if y_position < 50:
            pdf.showPage()  # Create a new page
            y_position = 750

    # Finalize the PDF
    pdf.save()

    # Create download button
    buffer.seek(0)
    st.download_button(
        label="Download Report",
        data=buffer,
        file_name="financial_insights_report.pdf",
        mime="application/pdf"
    )
