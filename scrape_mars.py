#import libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests 
import splinter
import selenium
import time

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = splinter.Browser('chrome', **executable_path, headless=False)
    
    #mars articles
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    mars = browser.html
    soup = BeautifulSoup(mars, 'html.parser')

    toptitle = soup.find_all('div', class_= 'content_title')[0].text
    toparticle = soup.find_all('div', class_= 'article_teaser_body')[0].text
    #time.sleep(1)
    
    #jpl featured image
    j_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(j_url)
    jpl = browser.html
    soup = BeautifulSoup(jpl, 'html.parser')
    art = soup.find('article', class_='carousel_item')
    string =  art['style'].split("'")[1]
    featured = 'https://www.jpl.nasa.gov' + string
    #time.sleep(1)
    
    #mars weather tweet
    t_url = 'https://twitter.com/marswxreport?lang=en'
    page = requests.get(t_url)
    html = page.text
    soup = BeautifulSoup(html, 'html.parser')
    first = soup.find('p', class_= 'TweetTextSize').text
    toptweet = first.split('pic.twitter')[0]
    
    #mars fact table
    m_url = 'https://space-facts.com/mars/'
    marsdf = pd.read_html(m_url)[1]
    marsdf.columns = ['Property', 'Value']
    marsdf.set_index('Property', inplace = True)
    marstable = marsdf.to_html(classes = 'html_table html_table-striped')
    marstable.replace('\n', '')
    
    #mars image urls
    #mars hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('Cerberus Hemisphere')
    link = browser.find_link_by_text('Sample')
    cerb = link[0]['href']
    browser.back()
    time.sleep(1)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere')
    link = browser.find_link_by_text('Sample')
    schap = link[0]['href']
    browser.back()
    time.sleep(1)
    browser.click_link_by_partial_text('Syrtis Major')
    link = browser.find_link_by_text('Sample')
    syrt = link[0]['href']
    browser.back()
    time.sleep(1)
    browser.click_link_by_partial_text('Valles Marineris')
    link = browser.find_link_by_text('Sample')
    vm = link[0]['href']

    
    mars_dict = {
        "top_headline" : toptitle,
        "top_article" : toparticle,
        "featured_image": featured,
        "Current_weather" : toptweet,
        "Mars_facts" : marstable,
        "img_1_title": "Cerberus Hemisphere Enhanced",
        "img_1_url": cerb,
        "img_2_title": "Schiaparelli Hemisphere Enhanced",
        "img_2_url": schap,
        "img_3_title": "Syrtis Major Hemisphere Enhanced",
        "img_3_url": syrt,
        "img_4_title": "Valles Marineris Hemisphere Enhanced",
        "img_4_url": vm
    }
    return mars_dict