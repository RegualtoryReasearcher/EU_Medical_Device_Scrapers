"""
Purpose:
    This script scrapes a Dutch medical website for warnings related to medical devices and saves the scraped data to a CSV file.

Author: Niamh McVey
Date: 2023/05/01
Usage:
    python dutch_scraper_main.py

Requirements:
    - Python 3.x
    - requests
    - BeautifulSoup
    - csv

Disclaimer:
    This script should be used in compliance with the website's terms of service.
"""

import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit

def get_data_page(url):
    """
    Fetches data from a specified URL and extracts relevant warning information about medical devices.

    Args:
        url (str): The URL to fetch the data from.

    Returns:
        tuple: A tuple containing a list of dictionaries for scraped data, and the next URL to scrape, if available.
    """

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        session = requests.Session()

        data_list = []

        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        link_elements = soup.find_all('a', class_='publication')

        for link in link_elements:
            title = link.find('h3').text.strip()

            warning_text = link.find('p').text.strip()

            date = link.find('p', class_='meta').text.strip().split('|')[-1].strip()

            data = {
                "title": title,
                "warning_text": warning_text,
                "date": date,
            }

            data_list.append(data)

        next_link_element = soup.find('li', class_='paging__unit paging__unit--next')

        if next_link_element:
             next_link = next_link_element.find('a')
             if next_link:
                   next_url = next_link.get('href')  # use absolute path directly
                   print("Next URL found:", next_url)
             else:
                   next_url = None
                   print("No <a> tag found in the next link element.")
        else:
            next_url = None
            print("No next link element found.")

        return data_list, next_url

    except Exception as e:
        print("Error occurred: ", e)
        return [], None



def get_data(start_url):
    """
    Aggregates data by scraping multiple pages starting from the given URL.

    Args:
        start_url (str): The initial URL to start scraping from.

    Returns:
        list: A list containing dictionaries of scraped data.
    """

    data_list = []
    next_url = start_url
    while next_url:
        print(f"Fetching data from page: {next_url}")
        data_page, next_url = get_data_page(next_url)
        data_list.extend(data_page)
    return data_list
    

def write_to_csv(data, filename):
    """
    Writes the gathered data to a CSV file.

    Args:
        data (list): List of dictionaries containing the scraped data.
        filename (str): The name of the CSV file to write the data to.

    Returns:
        None
    """

    print(f"Writing data to: {filename}")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        keys = data[0].keys()
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

# Define start URL
start_url = 'https://www.igj.nl/onderwerpen/waarschuwingen-medische-hulpmiddelen/documenten?trefwoord=&startdatum=01-01-2013&einddatum=&onderwerp=Alle+onderwerpen&onderdeel=Alle+onderdelen&type=Alle+publicaties'

# Fetch data
data = get_data(start_url)

# Write all data to CSV
write_to_csv(data, "devices_data.csv")

