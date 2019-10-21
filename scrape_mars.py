from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    return webdriver.Chrome("windows/chromedriver")


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://..."
    browser.get(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.page_source
    soup = bs(html, "html.parser")

    ...

    # Close the browser after scraping
    browser.close()

    # Return results
    return mars_data
