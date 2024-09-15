import streamlit as st
import yfinance as yf  # Example for fetching stock data

def get_market_insights():
    st.title("Market & Investment Insights")

    # Example: Input field for stock ticker symbol
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)")

    # Fetch data from Yahoo Finance using yfinance
    if ticker:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Safely access stock_info fields with fallback values
        short_name = stock_info.get('shortName', 'N/A')
        regular_market_price = stock_info.get('regularMarketPrice', 'N/A')
        market_cap = stock_info.get('marketCap', 'N/A')
        fifty_two_week_high = stock_info.get('fiftyTwoWeekHigh', 'N/A')
        fifty_two_week_low = stock_info.get('fiftyTwoWeekLow', 'N/A')

        st.subheader(f"Insights for {short_name}")
        st.write(f"**Current Price**: ${regular_market_price}")
        st.write(f"**Market Cap**: ${market_cap}")
        st.write(f"**52 Week High**: ${fifty_two_week_high}")
        st.write(f"**52 Week Low**: ${fifty_two_week_low}")
        
        st.subheader("Recent Market News")
        news = stock.news
        if news:
            for article in news[:5]:  # Show the 5 most recent news articles
                st.write(f"- {article['title']} ([Read more]({article['link']}))")
        else:
            st.write("No recent news found.")
    else:
        st.write("Enter a valid stock ticker symbol to get insights.")
