import yfinance as yf
import streamlit as st

def get_stock_screener():
    st.title('Stock Screener')

    # Add filters for the stock screener
    st.sidebar.header('Filters')
    
    market_cap_min = st.sidebar.number_input('Minimum Market Cap (in billions)', min_value=0, value=10)
    market_cap_max = st.sidebar.number_input('Maximum Market Cap (in billions)', min_value=0, value=500)
    pe_ratio_min = st.sidebar.number_input('Minimum PE Ratio', min_value=0, value=10)
    pe_ratio_max = st.sidebar.number_input('Maximum PE Ratio', min_value=0, value=30)
    dividend_yield_min = st.sidebar.number_input('Minimum Dividend Yield (%)', min_value=0.0, value=0.0)
    dividend_yield_max = st.sidebar.number_input('Maximum Dividend Yield (%)', min_value=0.0, value=10.0)
    
    # Placeholder for filtered stocks
    st.header('Filtered Stocks')
    
    # Example: Use Yahoo Finance to screen stocks based on the input filters
    stocks = yf.Tickers('AAPL MSFT TSLA')  # Sample list of stocks to screen
    stock_data = {ticker: stocks.tickers[ticker].info for ticker in stocks.symbols}

    filtered_stocks = []
    
    for ticker, info in stock_data.items():
        if (info['marketCap'] / 1e9 >= market_cap_min and info['marketCap'] / 1e9 <= market_cap_max and
            info['trailingPE'] >= pe_ratio_min and info['trailingPE'] <= pe_ratio_max and
            info['dividendYield'] >= dividend_yield_min and info['dividendYield'] <= dividend_yield_max):
            filtered_stocks.append((ticker, info))
    
    if filtered_stocks:
        st.write(f'Found {len(filtered_stocks)} stocks matching the criteria:')
        for stock in filtered_stocks:
            st.write(stock)
    else:
        st.write('No stocks found matching the criteria.')
