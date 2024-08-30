import logging
import os
import re
from typing import List, Set, Tuple

import pandas
import requests
import yfinance
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool

from financial_insights.src.tools import coerce_str_to_list
from financial_insights.src.utilities_retrieval import get_qa_response
from financial_insights.streamlit.constants import *

logging.basicConfig(level=logging.INFO)

RETRIEVE_HEADLINES = False


class YahooFinanceNewsInput(BaseModel):
    """Input for the YahooFinanceNews tool."""

    simbol_list: List[str] | str = Field(
        description='A list of ticker symbols to search.',
    )
    user_query: str = Field(description='The original user query.')


def filter_texts_set(texts: Set[str]) -> List[str]:
    """
    Filter a set of texts and combine them into a list of chunks.

    Args:
        texts: A set of texts to filter.

    Returns:
        A list of chunks.

    Raises:
        TypeError: If the input `texts` is not a set or a string.
    """
    # Check inputs
    assert isinstance(texts, set), TypeError(f'Input must be of type set. Got {type(texts)}.')
    assert all(isinstance(text, str) for text in texts), TypeError(f'Input must be of type str.')

    filtered_texts = set()
    for text in texts:
        chunks = filter_text(text)
        for chunk in chunks:
            filtered_texts.add(chunk)
    return list(filtered_texts)


def filter_text(text: str) -> List[str]:
    """
    Split a text into chunks of MAX_CHUNK_SIZE.

    Args:
        The text to split into chunks.

    Returns:
        A list of chunks.

    Raises:
        TypeError: If the input `text` is not a string.
    """
    # Check inputs
    assert isinstance(text, str), TypeError(f'Input must be of type str. Got {type(text)}.')

    filtered_texts: List[str] = list()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Instantiate the text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=[
            r'\n\n',  # Split on double newlines (paragraphs)
            r'(?<=[.!?])\s+(?=[A-Z])',  # Split on sentence boundaries
            r'\n',  # Split on single newlines
            r'\s+',  # Split on whitespace
            r'',  # Split on characters as a last resort
        ],
        is_separator_regex=True,
    )

    # Split the long text into smaller chunks
    chunks = splitter.split_text(text)

    return chunks


def clean_text(text: str) -> str:
    """Clean the text by removing extra spaces, newlines, and special characters."""

    # Check inputs
    assert isinstance(text, str), TypeError(f'Input must be of type str. Got {type(text)}.')

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return ' '.join(text.split())


@tool(args_schema=YahooFinanceNewsInput)
def scrape_yahoo_finance_news(simbol_list: List[str] | str, user_query: str) -> Tuple[str, List[str]]:
    """
    Tool that searches financial news on Yahoo Finance ny webscraping.

    Useful for when you need to find financial news about a public company.

    Args:
        company_list: List of tickers about which to search for financial news.
            For example, AAPL for Apple, MSFT for Microsoft.
        user_query: The search query to be used in the search bar on Yahoo Finance.

    Returns:

    Raises:
        TypeError: If `symbol_list` is not a list of strings or `user_query` is not a string.
    """
    # Check inputs
    assert isinstance(simbol_list, (list, str)), TypeError(
        f'Input must be of type `list` or `str`. Got {type(simbol_list)}.'
    )

    # If `symbol_list` is a string, coerce it to a list of strings
    symbol_list = coerce_str_to_list(simbol_list)

    assert all(isinstance(symbol, str) for symbol in symbol_list), TypeError(
        'All elements in `symbol_list` must be of type str.'
    )
    assert isinstance(user_query, str), TypeError(f'Input must be of type str. Got {type(user_query)}.')

    # Define the URL of the Yahoo Finance news page
    main_url = 'https://finance.yahoo.com/news'

    general_urls = []
    singular_urls = []

    # For each symbol determine the list of URLs to scrape
    if symbol_list is not None and len(symbol_list) > 0:
        for symbol in symbol_list:
            try:
                general_urls.append(f'https://finance.yahoo.com/quote/{symbol}/')
                news = yfinance.Ticker(symbol).news
                singular_urls.extend([news[i]['link'] for i, _ in enumerate(news)])
            except:
                pass
    else:
        general_urls.append(main_url)

    # Initialize lists to store the extracted data
    headlines = set()
    h2_headings = set()
    h3_headings = set()
    paragraphs = set()

    link_urls = list()

    # Webscraping by url
    for url in general_urls + singular_urls:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links on the page
            if url in general_urls:
                # Find all the links mentioned in the webpage
                links = soup.find_all('a')
                link_urls.extend([link['href'] for link in links])
            else:
                link_urls.append(url)
            logging.info('News articles have been successfully scraped')
        else:
            logging.warning(f'Failed to retrieve the page. Status code: {response.status_code}')

    # Remove duplicate URLs from the list of links
    link_urls = list(set(link_urls))
    # Filter links
    link_urls = [
        link_url
        for link_url in link_urls
        if link_url.startswith('https://finance.yahoo.com/news/')
        or link_url.startswith('https://finance.yahoo.com/quote/')
    ]

    data = list()
    # Loop through the links to visit each page and extract headlines
    for link_url in link_urls:
        # Send an HTTP GET request to the link
        link_response = requests.get(link_url)
        if link_response.status_code == 200:
            # Parse the content of the link's page
            soup = BeautifulSoup(link_response.content, 'html.parser')

            if RETRIEVE_HEADLINES:
                # Find elements with 'data-test-locator="headline"'
                headline_elements = soup.find_all(attrs={'data-test-locator': 'headline'})
                # Extract and append the headline text to the headlines list
                for headline_element in headline_elements:
                    text = clean_text(headline_element.text.strip())
                    headlines.add(text)
                    filtered_texts = filter_text(text)
                    for filtered_text in filtered_texts:
                        data.append({'type': 'h1', 'url': link_url, 'text': filtered_text})

                # Find and extract all <h2> headings
                for h2_tag in soup.find_all('h2'):
                    text = clean_text(h2_tag.get_text(strip=True))
                    h2_headings.add(text)
                    filtered_texts = filter_text(text)
                    for filtered_text in filtered_texts:
                        data.append({'type': 'h2', 'url': link_url, 'text': filtered_text})

                # Find and extract all <h3> headings
                for h3_tag in soup.find_all('h3'):
                    text = clean_text(h3_tag.get_text(strip=True))
                    h3_headings.add(text)
                    filtered_texts = filter_text(text)
                    for filtered_text in filtered_texts:
                        data.append({'type': 'h3', 'url': link_url, 'text': filtered_text})

            # Find and extract all <p> paragraphs
            for p_tag in soup.find_all('p'):
                text = clean_text(p_tag.get_text(strip=True))
                paragraphs.add(text)
                filtered_texts = filter_text(text)
                for filtered_text in filtered_texts:
                    data.append({'type': 'p', 'url': link_url, 'text': filtered_text})

            logging.info('News articles have been successfully scraped')
        else:
            logging.warning(f'Failed to retrieve the page. Status code: {response.status_code}')

    # Filter all texts
    headlines_list = filter_texts_set(headlines)
    h2_headings_list = filter_texts_set(h2_headings)
    h3_headings_list = filter_texts_set(h3_headings)
    paragraphs_list = filter_texts_set(paragraphs)

    # Create a DataFrame from the lists
    df = pandas.DataFrame({'News': headlines_list + h2_headings_list + h3_headings_list + paragraphs_list})
    df.drop_duplicates().reset_index(drop=True, inplace=True)

    # Save the DataFrame to a CSV file
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    df.to_csv(YFINANCE_NEWS_CSV_PATH, index=False)

    # Save the data to a text file in the specified order
    with open(YFINANCE_NEWS_TXT_PATH, 'w') as file:
        if RETRIEVE_HEADLINES:
            file.write('=== Headlines ===\n')
            for item in headlines_list:
                file.write(f'{item}\n')

            file.write('\n=== H2 Tags ===\n')
            for item in h2_headings_list:
                file.write(f'{item}\n')

            file.write('\n=== H3 Tags ===\n')
            for item in h3_headings_list:
                file.write(f'{item}\n')

        # Always include the paragraphs
        file.write('\n=== Paragraphs ===\n')
        for item in paragraphs_list:
            file.write(f'{item}\n')

    # Convert the list to a DataFrame
    df_text_url = pandas.DataFrame(data)
    # Save the DataFrame to a CSV file
    df_text_url.to_csv(WEB_SCRAPING_PATH, index=False)

    logging.info('News from Yahoo Finance successfully extracted and saved.')

    # Load the dataframe from the text file
    try:
        df = pandas.read_csv(WEB_SCRAPING_PATH)
    except FileNotFoundError:
        logging.error('No scraped data found.')

    # Convert DataFrame rows into Document objects
    documents = []
    for _, row in df.iterrows():
        document = Document(
            page_content=row['text'],
            metadata={'url': row['url'], 'type': row['type']},
        )
        documents.append(document)

    # Get the QA response
    response = get_qa_response(user_query, documents)

    # Assert that response is indexable
    assert isinstance(response, dict), 'QA response is not a dictionary.'

    # Extract the answer from  the QA response
    answer = response['answer']

    # Extract the urls from the QA response
    url_list = [doc.metadata['url'] for doc in response['context']]

    return answer, url_list
