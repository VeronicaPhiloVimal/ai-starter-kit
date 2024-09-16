from fpdf import FPDF
import os

def generate_pdf_report(session_state):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Smart Financial Plan Report", ln=True, align="C")

    # User Profile
    if 'user_profile' in session_state:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="User Financial Profile", ln=True, align="L")
        pdf.set_font("Arial", '', 12)
        for key, value in session_state['user_profile'].items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Goal-Based Financial Plan
    if 'goal_based_plan' in session_state:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Goal-Based Financial Plan", ln=True, align="L")
        pdf.set_font("Arial", '', 12)
        for goal, details in session_state['goal_based_plan'].items():
            pdf.cell(200, 10, txt=f"{goal}: {details}", ln=True)

    # Market Insights
    if 'market_insights' in session_state:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Market Insights", ln=True, align="L")
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, session_state['market_insights'])

    # Investment Recommendations
    if 'investment_recommendations' in session_state:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Investment Recommendations", ln=True, align="L")
        pdf.set_font("Arial", '', 12)
        for rec in session_state['investment_recommendations']:
            pdf.cell(200, 10, txt=rec, ln=True)

    # Stock Data Analysis
    if 'stock_data_analysis' in session_state:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Stock Data Analysis", ln=True, align="L")
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, session_state['stock_data_analysis'])

    # Save the PDF
    pdf_output_path = "/tmp/financial_plan_report.pdf"
    pdf.output(pdf_output_path)

    return pdf_output_path
