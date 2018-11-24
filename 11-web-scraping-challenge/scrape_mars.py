import pymongo
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

# setup mongo connection
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    data = {}

    # NASA Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    html = browser.html
    soup = bs(html, 'html.parser')
    
    posts = soup.find_all("div", class_="list_text")
    
    title = []
    para = []

    for post in posts:
        title.append(post.a.text)
        para.append(post.find("div", class_="article_teaser_body").text)
        
    # Image URL
    # URL varies depending on what the web browser opens
    url_image = "https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA18906"    

    response_image1 = requests.get(url_image)
    soup_image1 = bs(response_image1.text, 'lxml')

    results_image = soup_image1.find_all("figure", class_="lede")

    image_url = []
    for image in results_image:
        image_url.append(image.a["href"])

        for url in image_url:
            featured_image_url= "https://www.jpl.nasa.gov"+url

    # Mars Weather
    target_user = "@MarsWxReport"
    public_tweets = api.user_timeline(target_user)

    weather_tweet = []

    for tweet in public_tweets:
        weather_tweet.append(tweet["text"])

    # Facts about Mars
    # Import as Dependencies and HTML

    # Mars Hemisphere
    url_cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    url_schiaparelli = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    url_syrtis = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    url_valles = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"

    url_hemisphere = [url_cerberus, url_schiaparelli, url_syrtis, url_valles]

    for url in url_hemisphere:
        response_hemisphere = requests.get(url)
        soup_hemisphere = bs(response_hemisphere.text, 'lxml')
        
        results_hemisphere = soup_hemisphere.find_all("div", class_="container")
        
        for result in results_hemisphere:
            hemi_title = result.h2.text
            hemi_img_url = result.find("img", class_="wide-image")["src"]

    data = {
        "news_title": title[0],
        "news_text": para[0],
        "featured_image": featured_image_url,
        "mars_weather": weather_tweet[0],
        "hemi_title": hemi_title,
        "img_url": "https://astrogeology.usgs.gov" + hemi_img_url
    } 

    return data



