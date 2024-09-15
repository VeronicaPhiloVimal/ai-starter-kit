# financial_assistant/streamlit/app_goal_planning.py

import streamlit as st

def generate_goal_based_plan():
    st.title("Goal-Based Financial Plan")

    # Example fields for goal-based financial planning
    goal_name = st.text_input("Enter your financial goal (e.g., Buy a house, Retirement)")
    goal_amount = st.number_input("Enter the amount needed to achieve this goal ($)", min_value=0)
    target_year = st.number_input("Enter the target year to achieve this goal", min_value=2024)

    # Simple estimation of how much to save each year to reach the goal
    current_year = 2024
    years_left = target_year - current_year
    if years_left > 0:
        yearly_saving_needed = goal_amount / years_left
        st.write(f"You need to save approximately ${yearly_saving_needed:.2f} per year to reach your goal.")
    else:
        st.warning("The target year should be in the future.")

    # Store the goal in session state
    if st.button("Save Goal"):
        st.session_state["financial_goal"] = {
            "goal_name": goal_name,
            "goal_amount": goal_amount,
            "target_year": target_year,
            "yearly_saving_needed": yearly_saving_needed if years_left > 0 else None
        }
        st.success("Goal-based financial plan generated successfully!")
