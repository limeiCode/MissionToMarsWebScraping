# Dependencies: import necessary libraries
from selenium import webdriver  # Web Scraping Framework # selenium webdriver API
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    return webdriver.Chrome("windows/chromedriver")


def scrape():
    browser = init_browser()
    marsdata_scrp_dict = {}
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
    marsdata_scrp_dict["latestnews_title"] = latestnews_title
    marsdata_scrp_dict["latestnews_p"] = latestnews_p


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
    marsdata_scrp_dict["featured_image_url"] = featured_image_url

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
    marsdata_scrp_dict["latestmarsweather_tweet"] = latestmarsweather_tweet


    # <4> Mars Facts
    # use Pandas to scrape the {table} containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['fact', 'value']
    # df = df.iloc[2:] # clean
    df.set_index('fact', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')
    # df.to_html('table.html')
    # print(type(html_table))

    soup = bs(html_table, 'html.parser').tbody
    # print(soup.prettify())
    # tablerow_list = soup.find_all('tr')
    tablerowth_list = soup.find_all('th')
    # print(tablerowth_list)
    tablerowtd_list = soup.find_all('td')
    # print(tablerowtd_list)

    tablerowthvl_list=[]
    tablerowtdvl_list=[]
    tablerowthvlvl_list=[]
    tablerowtdvlvl_list=[]

    for r in tablerowth_list:
        n = str(r)[4:]
        tablerowthvl_list.append(n)
    for r in tablerowthvl_list:
        n = str(r)[:-6]
        tablerowthvlvl_list.append(n)    
    # print(tablerowthvlvl_list)

    for r in tablerowtd_list:
        n = str(r)[4:]
        tablerowtdvl_list.append(n)
    for r in tablerowtdvl_list:
        n = str(r)[:-6]
        tablerowtdvlvl_list.append(n)    
    # print(tablerowtdvlvl_list)

    th_and_td = zip(tablerowthvlvl_list,tablerowtdvlvl_list)
    # print(tuple(th_and_td))

    thtd_dict = {}
    thtd_dictlist =[]
    for i in th_and_td:
        l=list(i)    
        thtd_dict["fact"] = l[0]
        thtd_dict["value"] =l[1]    
        thtd_dictlist.append(thtd_dict.copy())  # !!.copy()

    marsdata_scrp_dict["thtd_dictlist"] = thtd_dictlist


    # <5> Mars Hemispheres
    # Jason: Looks like the for the week 12 HW that the Mars Hemispheres link (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) is unreliable. If it is not working for you, then choose 4 images from this link instead: https://www.usgs.gov/centers/astrogeology-science-center/multimedia (edited) 
    # obtain {high} resolution images for each of Mar's hemispheres.
    # You will need to {{click each of the links}} to the hemispheres in order to find the image url to the {full resolution image}.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.get(url)
    # Scrape page into Soup
    html = browser.page_source
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    # Examine the results, then determine element that contains sought info
    # print(soup.body.prettify())
    hemisphere_dictlist = []
    hemisphere_dict = {}
    item_list = soup.find_all('div', class_="item")
    # click each of the links to the hemispheres in order to find the image url to the {full resolution image ???
    for m in item_list:
        hemisphere_dict["title"] = m.div.a.h3.text
        pageurlstr = "https://astrogeology.usgs.gov" + m.div.a["href"] # is the url for a page not for a image!! need further scape from this page to get image url!!
    # click each of the links to the hemispheres in order to find the image url to the {full resolution image ???
    #     pageurlstr.click() # AttributeError: 'str' object has no attribute 'click'  ???  
    # https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced
    # =>
    # https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg    
        browser.get(pageurlstr)  # not get this new page, still the previous one???
        htmlnew = browser.page_source
        soup = bs(htmlnew, 'html.parser').body
        imageurlstr = "https://astrogeology.usgs.gov" + soup.find('img', class_="wide-image")["src"]
        hemisphere_dict["img_url"] = imageurlstr
        hemisphere_dictlist.append(hemisphere_dict.copy())
        
    marsdata_scrp_dict["hemisphere_dictlist"] = hemisphere_dictlist
                                                    


    # Close the browser after scraping
    browser.close()

    # Return results
    return marsdata_scrp_dict
