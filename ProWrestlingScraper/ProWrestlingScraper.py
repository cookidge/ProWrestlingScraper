#!/usr/bin/env python

"""ProWrrestlingScraper.py: Prototype scraper of Pro-Wrestling data from www.profightdb.com"""

__author__      = "James Cooke"
__copyright__   = "Copyright 2019"

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# site http://www.profightdb.com
# wrestlers a to z /atoz.html?term=a&start=0
# term runs a through to z, start is wrestlers on the page, increments of 100

domain = "http://www.profightdb.com/atoz.html"
alpha = "abcdefghijklmnopqrstuvwxyz"

# loop through each page
for index in range(len(alpha)):
    page = "?term=" + alpha[index] # retrieve page
    params = page + "&start="
    currentUrl = domain + params # build page url

    # retrieve page HTML
    response = requests.get(currentUrl)                     # retrieve page html
    soup = BeautifulSoup(response.text, "html.parser")
    lasttag = soup.find_all("a",text = "last", limit = 1)   # retrieve href from last page <a> tag

    if len(lasttag) > 0:
        lastlink = lasttag[0].get('href')
        last = lastlink.replace(params, "")
        itr = int(last) / 100                               # calculate number of pages
    else:
        itr = 0

    start = 0                                               # default start


    # loop through number of pages
    for cur in range(int(itr)+1):
        print(currentUrl + str(start))                      # set page for [a,b,c] number [1,2,3] i.e. term=a&start=700                
        start = start + 100

time.sleep(1)


	    # loop through each wrestler

    		# store data (name etc) in row, and retrieve url

	        # access wrestler url - scrape data on wrestler




