#%% [markdown]
# ## Import Dependencies

#%%
import pandas as pd
import requests
import pymongo
import os
import tweepy
import json
import numpy as np

from config import consumer_key, consumer_secret, access_token, access_token_secret
from datetime import datetime
from splinter import Browser
from bs4 import BeautifulSoup as bs
from pprint import pprint

# Setup Tweepy Authentication 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#%% [markdown]
# ## Step 1 - Scraping

#%%
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


#%%
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


#%%
db = client.space_db
collection = db.articles

#%% [markdown]
# ## NASA Mars News

#%%
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)


#%%
# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'lxml')


#%%
results = soup.find_all("div", class_="list_text")


#%%
html = browser.html
soup = bs(html, 'html.parser')

posts = soup.find_all("div", class_="list_text")

title = []
para = []

for post in posts:
    title.append(post.a.text)
    para.append(post.find("div", class_="article_teaser_body").text)

    article ={
        "news_title": title[0],
        "news_text": para[0]
    }

#     news_title = title[0]
#     news_p = para[0]


#%%
print(article["news_title"])
print(article["news_text"])


#%%
for result in results:
    title = result.a.text
    para = result.find("div", class_="article_teaser_body").text
    
    article = {
        "news_title": title,
        "news_paragraph": para
    }
    
    print("---------------------------------")
    print(f'{title}')
    print(f'{para}')

#%% [markdown]
# ## Finding the Images URL

#%%
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url2)


#%%
# Retrieve page with the requests module
response_image = requests.get(url2)

# Create BeautifulSoup object; parse with 'lxml'
soup_image = bs(response_image.text, 'lxml')


#%%
browser.click_link_by_partial_text('FULL IMAGE')


#%%
browser.click_link_by_partial_text('more info')


#%%
# URL varies depending on what the web browser opens
url_image = "https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA18185"


#%%
# Retrieve page with the requests module
response_image1 = requests.get(url_image)

# Create BeautifulSoup object; parse with 'lxml'
soup_image1 = bs(response_image1.text, 'lxml')


#%%
results_image = soup_image1.find_all("figure", class_="lede")


#%%
# Scarping the image url
image_url = []
for image in results_image:
    image_url.append(image.a["href"])


#%%
image_url


#%%
# Adding the url into images
for url in image_url:
    featured_image_url= "https://www.jpl.nasa.gov"+url
    print(featured_image_url)

#%% [markdown]
# ## Mars Weather

#%%
target_user = "@MarsWxReport"


#%%
public_tweets = api.user_timeline(target_user)


#%%
weather_tweet = []

for tweet in public_tweets:
    weather_tweet.append(tweet["text"])


#%%
mars_weather = weather_tweet[0]
print(mars_weather)

#%% [markdown]
# ## Mars Facts

#%%
url_facts = "https://space-facts.com/mars/"


#%%
tables = pd.read_html(url_facts)
tables


#%%
df = tables[0]


#%%
df_clean = df.set_index(0)
df_clean.index.name=None


#%%
df_clean = df_clean.rename(columns={1: "Values"})
df_clean


#%%
html_table = df_clean.to_html()


#%%
html_table.replace('\n', '')


#%%
df_clean.to_html('mars_facts.html')

#%% [markdown]
# ## Mars Hemisphere

#%%
url_cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
url_schiaparelli = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
url_syrtis = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
url_valles = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"


#%%
url_hemisphere = [url_cerberus, url_schiaparelli, url_syrtis, url_valles]

for url in url_hemisphere:
    response_hemisphere = requests.get(url)
    soup_hemisphere = bs(response_hemisphere.text, 'lxml')
    
    results_hemisphere = soup_hemisphere.find_all("div", class_="container")
    
    for result in results_hemisphere:
        title = result.h2.text
        img_url = result.find("img", class_="wide-image")["src"]
        
        hemisphere_image_urls = {
            "title": title,
            "img_url": "https://astrogeology.usgs.gov"+img_url
        }
        
        print(hemisphere_image_urls)


#%%
print(hemisphere_image_urls["img_url"])


