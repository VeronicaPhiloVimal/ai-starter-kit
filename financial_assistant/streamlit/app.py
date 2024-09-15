import datetime
import os
import sys
import time

import weave
import yaml

# Main directories
current_dir = os.path.dirname(os.path.abspath(__file__))
kit_dir = os.path.abspath(os.path.join(current_dir, '..'))
repo_dir = os.path.abspath(os.path.join(kit_dir, '..'))
sys.path.append(kit_dir)
sys.path.append(repo_dir)

import streamlit
from streamlit_extras.stylable_container import stylable_container

from financial_assistant.src.tools import get_logger
from financial_assistant.streamlit.app_stock_data import get_stock_data_analysis
from financial_assistant.streamlit.app_stock_database import get_stock_database
from financial_assistant.streamlit.constants import *
from financial_assistant.streamlit.utilities_app import (
    clear_cache,
    create_temp_dir_with_subdirs,
    display_directory_contents,
    get_blue_button_style,
    initialize_session,
    schedule_temp_dir_deletion,
    set_css_styles,
    submit_sec_edgar_details,
)
from utils.visual.env_utils import are_credentials_set, env_input_fields, save_credentials

# Additional feature imports
from financial_assistant.streamlit.app_user_profile import generate_user_profile
from financial_assistant.streamlit.app_goal_planning import generate_goal_based_plan
from financial_assistant.streamlit.app_market_insights import get_market_insights
from financial_assistant.streamlit.app_investment_recommendations import get_investment_recommendations
from financial_assistant.streamlit.app_ai_report import generate_ai_report


# Initialize Weave with your project name
if os.getenv('WANDB_API_KEY') is not None:
    weave.init('sambanova_financial_assistant')

# Load the config
with open(CONFIG_PATH, 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)
# Get the production flag
prod_mode = config['prod_mode']

logger = get_logger()

def main() -> None:
    # Initialize session
    initialize_session(streamlit.session_state, prod_mode)

    # Streamlit app setup
    streamlit.set_page_config(
        page_title='Smart Financial Plan Assistant',
        page_icon=SAMBANOVA_LOGO,
        layout='wide',
    )

    # Set CSS styles
    set_css_styles()

    # Add SambaNova logo
    streamlit.logo(
        image=SAMBANOVA_LOGO,
        link=SAMBANOVA_LOGO,
        icon_image=SAMBANOVA_LOGO,
    )

    # Add sidebar
    with streamlit.sidebar:
        if not are_credentials_set():
            streamlit.markdown('Get your SambaNova API key [here](https://cloud.sambanova.ai/apis)')
            url, api_key = env_input_fields()
            if streamlit.button('Save Credentials', key='save_credentials_sidebar'):
                message = save_credentials(url, api_key, prod_mode)
                streamlit.success(message)
                streamlit.rerun()
        else:
            streamlit.success('Credentials are set')
            with stylable_container(
                key='blue-button',
                css_styles=get_blue_button_style(),
            ):
                if streamlit.button('Clear Credentials', key='clear_credentials'):
                    save_credentials('', '', prod_mode)
                    streamlit.success(r':orange[You have been logged out.]')
                    time.sleep(2)
                    streamlit.rerun()

        # Navigation menu
        menu = streamlit.radio(
            'Go to',
            [
                'Home',
                'User Financial Profile',
                'Goal-Based Financial Plan',
                'Market & Investment Insights',
                'Investment Recommendations',
                'Generative AI Report',
                'Stock Data Analysis',
                'Stock Database',
            ],
        )

    # Main app
    if menu == 'Home':
        streamlit.title('Smart Financial Plan Assistant')

        streamlit.write("""Welcome to the Smart Financial Plan Assistant, where you can explore a wide range
            of financial insights, market data, and personalized investment plans using AI-powered models.
        """)

    elif menu == 'User Financial Profile':
        generate_user_profile()

    elif menu == 'Goal-Based Financial Plan':
        generate_goal_based_plan()

    elif menu == 'Market & Investment Insights':
        get_market_insights()

    elif menu == 'Investment Recommendations':
        get_investment_recommendations()

    elif menu == 'Generative AI Report':
        generate_ai_report()

    elif menu == 'Stock Data Analysis':
        get_stock_data_analysis()

    elif menu == 'Stock Database':
        get_stock_database()

if __name__ == '__main__':
    main()
