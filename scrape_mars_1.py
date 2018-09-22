
# coding: utf-8

# In[1]:


# Import BeautifulSoup
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
from splinter import Browser

# In[2]:

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def render_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    r = driver.page_source
    return r


# In[3]:


# Import Splinter and set the chromedriver path

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
driver = webdriver.Chrome()


# In[4]:

def scrape():
    browser = init_browser()
    scraped_data = {}
    # Visit the following URL
    url = "https://mars.nasa.gov/news/"
    response = render_page(url)
    soup = bs(response, 'html.parser')


    # In[5]:


    # print(soup.prettify())


    # In[6]:


    # results = soup.find_all('div',class_="list_text")


    # # In[7]:


    # news_title = results[0].find('a').text
    news_title = soup.find('div',class_="content_title").text
    print(news_title)
    news_p = soup.find('div', class_="article_teaser_body").text
    print(news_p)


    # In[8]:


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.is_text_present('FULL IMAGE', wait_time=10)
    browser.click_link_by_partial_text('FULL IMAGE')
    # time.sleep(3)


    # In[9]:


    browser.is_text_present('more info', wait_time=10)

    browser.click_link_by_partial_text('more info')
    # time.sleep(3)


    # In[10]:


    browser.is_element_present_by_css('.lede', wait_time=10)

    browser.click_link_by_partial_href('.jpg')


    # In[11]:


    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find('img').get('src')
    print(featured_image_url)


    # In[12]:


    url = "https://twitter.com/marswxreport?lang=en"
    response = render_page(url)
    soup = bs(response, 'html.parser')


    # In[13]:


    # print(soup.prettify())


    # In[14]:


    mars_weather = soup.find('p',class_="tweet-text").text
    mars_weather


    # In[15]:


    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables


    # In[16]:


    df = tables[0]
    df.columns = ['Description','Value']
    df.set_index('Description', inplace=True)
    df.head()


    # In[17]:


    html_table = df.to_html()
    html_table.replace('\n', '')


    # In[18]:


    base_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(base_url)

    html = browser.html
    soup = bs(html, 'html.parser')


    # In[19]:


    hem_img_urls = []
    hem_dict = {'title': [], 'img_url': [],}

    titles = soup.find_all('h3')
    # print(titles)

    for t in titles:
        title = t.get_text()
    #     print(title)
        title_striped = title.strip('Enhanced')
        browser.click_link_by_partial_text(title)
        url = browser.find_link_by_partial_href('download')['href']
        hem_dict = {'title': title_striped, 'img_url': url}
        hem_img_urls.append(hem_dict)
        browser.visit(base_url)
    hem_img_urls

