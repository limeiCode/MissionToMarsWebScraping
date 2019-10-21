# Dependencies: import necessary libraries
from selenium import webdriver  # Web Scraping Framework # selenium webdriver API
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    return webdriver.Chrome("windows/chromedriver")


def scrape():
    browser = init_browser()
    marsdata_scrp = {}
    # <1>NASA Mars News:
    # Scrape the NASA Mars News Site and collect the {latest} News [Title] and [Paragraph Text].
    # Assign the text to variables that you can reference later.
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.get(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.page_source
    soup = bs(html, "html.parser")
    # find() is the later one, find_all() is all
    news_list = soup.find_all('div', class_='list_text')
    latestnews_title = news_list[0].find('div', class_='content_title').a.text
    latestnews_p = news_list[0].find('div', class_='article_teaser_body').text
    marsdata_scrp["latestnews_title"] = latestnews_title
    marsdata_scrp["latestnews_p"] = latestnews_p


    # <2> JPL Mars Space Images - Featured Image :
    # Use Selenium to navigate the site and find the image url for the {current Featured Mars Image} and assign the [url string] to a variable called featured_image_url.
    # Make sure to find the image url to the {full size .jpg image}.
    # Make sure to save a complete url string for this image.
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.get(url)

    # Scrape page into Soup
    html = browser.page_source
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    # Examine the results, then determine element that contains sought info
    # print(soup.body.prettify())
    imageurl_list = soup.find_all('footer')
    featured_image_url = 'https://www.jpl.nasa.gov' + \
        imageurl_list[0].find('a', class_='button fancybox')['data-fancybox-href']
    marsdata_scrp["featured_image_url"] = featured_image_url

    # <3> Mars Weather
    # scrape the {latest Mars weather tweet} from the page. Save the tweet text for the weather report as a variable called mars_weather.
    
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.get(url)
    # Scrape page into Soup
    html = browser.page_source
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    # Examine the results, then determine element that contains sought info
    # print(soup.body.prettify())
    tweet_list = soup.find_all('div',class_='js-tweet-text-container')
    latestmarsweather_tweet = tweet_list[0].find('p').text
    marsdata_scrp["latestmarsweather_tweet"] = latestmarsweather_tweet



    # Close the browser after scraping
    browser.close()

    # Return results
    return marsdata_scrp
