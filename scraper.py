"""This file will serve as the module for reading url collections
from the file and web scraping text content"""

# Import Packages

import PyPDF2
import requests
from bs4 import BeautifulSoup
from typing import List
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Get url from txt
def read_urls_from_file(file_path: Path = "./urls.txt") -> List[str]:
    """_summary_
    Read URL from a text data

    Args:
        file_path (Path, optional): _description_. Defaults to "./urls.txt".

    Returns:
        List[str]: _description_
    """
    with open(file_path, "r") as file:
        urls = [line.strip() for line in file]
        print(urls)
    return urls


# For Dynamic Website
def scrape_dyn_url(url: str):
    """_summary_

    Args:
        url (str): _description_
    """
    try:
        # Set up Selenium web driver

        # options = Options()
        options = webdriver.ChromeOptions()
        # options.headless = True
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        # Load Website
        driver.get(url)

        # Wait for the page to load (you might need to adjust the wait time)
        driver.implicitly_wait(10)

        # Get the page source after it has been fully rendered
        page_source = driver.page_source

        # Print the extracted text
        print(page_source)

        # extract data
        None
        # Close the web driver
        driver.quit()

    except Exception as e:
        print(f"Error accessing the website {e}")


# For Static Website
def scrape_stat_url(url: str):
    """_summary_

    Args:
        url (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        if "html" in url.lower():
            # Use BeautifulSoup to parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            text = soup.get_text()

            print(text)

            # Extract data
            None
        if "pdf" in url.lower():
            # Save file locally
            with open("file.pdf", "wb") as file:
                file.write(response.content)
            # Extract text from PDF
            with open("file.pdf", "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                text = ""
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                print(text)

            # Extract Data
            None
        else:
            text = None

    except requests.exceptions.RequestException as e:
        print(f"Couldn't acces website: {e} ")
    finally:
        return text
