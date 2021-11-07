import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 
from pprint import pprint


# Start by converting your Jupyter notebook into a Python script called scrape_mars.py
# with a function called scrape that will execute all of your scraping code from above 
# and return one Python dictionary containing all of the scraped data.
def scrape():

    dict_scrape = {}

    # ------------------------NASA Mars News-------------------------------------
    # url of page to scrape
    url = 'https://redplanetscience.com/'

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    time.sleep(1)
    
    # create beautiful soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    dict_scrape['news_recent_title'] = news_title
    dict_scrape['news_teaser'] = news_p
    
    browser.quit()

    #-------------------JPL Mars Space Images - Featured Image-------------------
    # url of page to scrape
    url = 'https://spaceimages-mars.com/'

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html

    # create beautiful soup object
    soup = BeautifulSoup(html, 'html.parser')
        
    f_img = soup.find('img', class_='headerimage fade-in')
    featured_image_url = url + f_img['src']
   
    dict_scrape['featured_mars_image'] = featured_image_url

    browser.quit()

    #-------------------------Mars Facts------------------------------------------
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)

    mars_df = tables[0]

    #change headers and index
    mars_df.columns = mars_df.iloc[0]
    mars_df = mars_df[1:]
    mars_df = mars_df.set_index('Mars - Earth Comparison')

    mars_html = mars_df.to_html(classes="table table-striped")
    dict_scrape['mars_facts'] = mars_html

    #-----------------------Mars Hemispheres---------------------------------------
    # url of page to scrape
    url = 'https://marshemispheres.com/'

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html

    # Create beautiful soup object
    soup = BeautifulSoup(html, 'html.parser')

    # List to store urls
    hemisphere_image_urls = []

    for i in range(4):
        dict = {}
        
        # find the divs with each link to click
        element = browser.find_by_css('a.product-item img.thumb')[i]
        # click link
        element.click()
        
        # get image
        image = browser.find_by_tag('img.wide-image')
        # get url of image
        img_url = image['src']
        print(img_url)
        # get title
        title = browser.find_by_tag('h2.title').text
        
        # make dict
        dict['Title'] = title
        dict['img_url'] = img_url
        hemisphere_image_urls.append(dict)
        #go back
        browser.back()
        
        dict_scrape['mars_hemispheres'] =  hemisphere_image_urls

    browser.quit() 
    #-----------------------------------------------------------------------------
    # print('*_*_*_*_*_*_*_*_*_*')
    # pprint(dict_scrape)
    # print('*_*_*_*_*_*_*_*_*_*')
    return dict_scrape

