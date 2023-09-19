"""
Metadata:

Script purpose:
This script fetches data about medical devices and writes the data to a CSV file.

Usage:
python3 unified_script.py

Dependencies:
- Python 3.6 or later
- BeautifulSoup4
- requests
- csv

Author: Niamh McVey
Date:2023/05/15
"""

# Importing required libraries
import requests
from bs4 import BeautifulSoup
import csv


# Function to remove invalid Unicode characters
def remove_surrogates(text):
    """Remove invalid Unicode characters from the text.

    Args:
        text (str): The text from which to remove invalid Unicode characters.

    Returns:
        str: The text with invalid Unicode characters removed.
    """
    return text.encode('utf-8', 'surrogatepass').decode('utf-8', 'ignore')


# Function to fetch a webpage
def get_page(url, headers):
    """Fetch the webpage content and return its parsed HTML.

    Args:
        url (str): The URL of the webpage to fetch.
        headers (dict): The HTTP headers to use for the request.

    Returns:
        BeautifulSoup object: The parsed HTML of the webpage.
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


# Function to scrape data from a single webpage
def scrape_page(soup):
    """Scrape medical device data from a given webpage's HTML.

    Args:
        soup (BeautifulSoup object): The parsed HTML of the webpage.

    Returns:
        list: A list of dictionaries, each containing the scraped data for one medical device.
    """
    data = []
    table = soup.find('table', attrs={'class': 'some_class'})  # Replace with actual class name
    if table:
        rows = table.findAll('tr')
        for row in rows[1:]:
            cols = row.findAll('td')
            record = {}
            record['column_1'] = remove_surrogates(cols[0].text.strip())  # Replace 'column_1' with actual column name
            # ... Do this for each column
            data.append(record)
    return data


# Function to find the URL of the next page
def get_next_page(soup):
    """Find and return the URL of the next page of data, if available.

    Args:
        soup (BeautifulSoup object): The parsed HTML of the current webpage.

    Returns:
        str or None: The URL of the next page, or None if it's the last page.
    """
    next_page_element = soup.find('a', attrs={'title': 'Next Page'})  # Replace with actual attribute values
    next_page_url = next_page_element.get('href') if next_page_element else None
    return next_page_url


# Function to save scraped data to a CSV file
def save_to_csv(data, filename):
    """Save the scraped medical device data to a CSV file.

    Args:
        data (list): The list of dictionaries containing the scraped data.
        filename (str): The name of the CSV file to create.

    Returns:
        None
    """
    if data:
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
    else:
        print("No data to write to CSV.")


# Main function to orchestrate the web scraping
def main():
    """Main function that orchestrates the entire web scraping process."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    base_url = "http://example.com/some_page"  # Replace with actual base URL
    all_data = []
    next_url = base_url

    # Loop through pages and scrape data
    while next_url:
        soup = get_page(next_url, headers)
        data = scrape_page(soup)
        all_data.extend(data)
        next_url = get_next_page(soup)

    # Save all scraped data to a CSV file
    save_to_csv(all_data, 'unified_data.csv')


# Entry point of the script
if __name__ == "__main__":
    main()
