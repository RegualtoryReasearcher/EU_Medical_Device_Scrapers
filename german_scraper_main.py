"""
Purpose:
    This script is designed to scrape information related to medical devices from the German Federal Institute for Drugs and Medical Devices (BfArM) website. The scraped data is then written to a CSV file.

Author: Niamh McVey
Date: 2023/05/01
Usage:
    python german_scraper_main.py

Requirements:
    - Python 3.x
    - requests
    - BeautifulSoup
    - csv

Disclaimer:
    This script should be used responsibly and in compliance with the website's terms of service.
"""

import csv
import requests
from bs4 import BeautifulSoup

def get_data_page(url):
    """
    Scrapes a single web page for information on medical devices including their date, device name, type, and reference.

    Args:
        url (str): The URL of the page to scrape.

    Returns:
        tuple: A list of dictionaries containing the scraped data and the URL of the next page to scrape, if available.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    session = requests.Session()

    data_list = []

    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    tr_elements = soup.find_all('tr')

    for tr in tr_elements:
        tds = tr.find_all('td')

        if len(tds) < 2:
            continue

        date = tds[0].get_text().strip()
        details_block = tds[1]

        link_element = details_block.find('a')
        device = link_element.get_text().strip() if link_element else "N/A"

        strong_elements = details_block.find_all('strong')
        if len(strong_elements) >= 2:
            device_type = strong_elements[0].next_sibling.strip()
            device_reference = strong_elements[1].next_sibling.strip()
        else:
            device_type = "N/A"
            device_reference = "N/A"

        data = {
            "date": date,
            "device": device,
            "device_type": device_type,
            "device_reference": device_reference,
        }

        data_list.append(data)

    next_link = soup.find('li', class_='c-navindex__item is-forward').find('a')

    if next_link:
        next_url = next_link.get('href')
    else:
        next_url = None

    return data_list, next_url


def get_data(start_url):
    """
    Scrapes multiple pages, starting from the provided URL, to accumulate a dataset on medical devices.

    Args:
        start_url (str): The URL to begin scraping.

    Returns:
        list: A list of dictionaries containing the aggregated data.
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
        filename (str): The name of the CSV file where the data will be stored.

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

def main():
    """
    Main function to coordinate the web scraping and data writing operations.
    """
    # Initial URL to begin scraping from
    start_url = 'http://www.bfarm.de/EN/Medical-devices/Tasks/Risk-assessment-and-research/Field-corrective-actions/_node.html'

    # Fetch the data
    print("Starting the data collection process...")
    data = get_data(start_url)

    # Write the fetched data to a CSV file
    if data:
        print("Writing the collected data to a CSV file...")
        write_to_csv(data, "devices_data.csv")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()

