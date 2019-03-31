#!/usr/bin/env python

"""ProWrrestlingScraper.py: Prototype scraper of Pro-Wrestling data from www.profightdb.com"""

__author__      = "James Cooke"
__copyright__   = "Copyright 2019"

import requests
import urllib.request
import datetime
import time
import re
import csv
from bs4 import BeautifulSoup

# function to write a row to a file
def write_csv(csvFile, row):

    # create quoted qualifying
    csv.register_dialect('quoted',
    quoting=csv.QUOTE_ALL,
    skipinitialspace=False)

    # write row to file
    with open(csvFile, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, dialect='quoted')
        writer.writerow(row)

    f.close()

# site http://www.profightdb.com
# wrestlers a to z /atoz.html?term=a&start=0
# term runs a through to z, start is wrestlers on the page, increments of 100

outputFile = r"C:\Users\James Cooke\Desktop\Projects\ProWrestlingDB\Wrestlers\wrestler_raw_data_" + str(datetime.datetime.now().date()) + ".csv"
site = "http://www.profightdb.com"
atoz = site + "/atoz.html"
alpha = "abcdefghijklmnopqrstuvwxyz"

# create output file header
outputHeader = ["NAME","PREFERRED_NAME","DATE_OF_BIRTH","PLACE_OF_BIRTH","NATIONALITY","GENDER","MATCHES","RING_NAMES"]
# write header to file
write_csv(outputFile,outputHeader)


# loop through each page
for index in range(len(alpha)):
    page = "?term=" + alpha[index] # retrieve page
    params = page + "&start="
    currentUrl = atoz + params # build page url

    # retrieve page HTML
    time.sleep(1)
    response = requests.get(currentUrl)                     # retrieve page html
    soup = BeautifulSoup(response.text, "html.parser")
    lasttag = soup.find_all("a",text = "last", limit = 1)   # retrieve href from last page <a> tag

    print("Retieved data for " + currentUrl)

    # if only one page - no last page href
    if len(lasttag) > 0:
        lastlink = lasttag[0].get('href')
        last = lastlink.replace(params, "")
        itr = int(last) / 100                               # calculate number of pages
    else:
        itr = 0

    start = 0                                               # default start

    # loop through number of pages
    for cur in range(int(itr)+1):
        
        # set current url
        currentUrl = atoz + params + str(start)            # set page for [a,b,c] number [1,2,3] i.e. term=a&start=700 
        time.sleep(1)
        pageresponse = requests.get(currentUrl)
        pagesoup = BeautifulSoup(pageresponse.text, "html.parser")
        wrestlertags = pagesoup.find_all("a", attrs = { "href" : re.compile("^/wrestlers/")})   # retrieve all wrestler urls on current page

        print("Retieved data for " + currentUrl)
        
        # loop through each wrestlertag
        for tag in wrestlertags:        
            
            wrestlerUrl = site + tag.get('href')               
            #wrestlerUrl = "http://www.profightdb.com/wrestlers/aj-styles-752.html"
            time.sleep(0.1)
            wrestlerresponse = requests.get(wrestlerUrl)
            wrestlersoup = BeautifulSoup(wrestlerresponse.text, "html.parser")

            wrestlerinfotags = wrestlersoup.find_all("td")                                              # retrieve all td tags on page
           
            for info in wrestlerinfotags:
                if str(info.text).upper().startswith("NAME"):  wr_Name = str(info.text).split(":")[1].strip()                    # store wrestler name
                if str(info.text).upper().startswith("PREFERRED NAME"): wr_PrefName = str(info.text).split(":")[1].strip()       # store preferred name
                if str(info.text).upper().startswith("DATE OF BIRTH"): wr_DOB = str(info.text).split(":")[1].strip()             # store date of birth
                if str(info.text).upper().startswith("PLACE OF BIRTH"): wr_POB = str(info.text).split(":")[1].strip()            # store place of birth
                if str(info.text).upper().startswith("NATIONALITY"): wr_Nationality = str(info.text).split(":")[1].strip()       # store nationality
                if str(info.text).upper().startswith("GENDER"): wr_Gender = str(info.text).split(":")[1].strip()                 # store gender
                if str(info.text).upper().startswith("MATCHES"): wr_Matches = str(info.text).split(":")[1].strip()               # store matches
                if str(info.text).upper().startswith("RING NAME(S)"): wr_RingNames = str(info.text).split(":")[1].strip()        # store ring name(s)

            print("Retieved data for " + wr_PrefName)

            # build row
            wrestler = [wr_Name,wr_PrefName,wr_DOB,wr_POB,wr_Nationality,wr_Gender,wr_Matches,wr_RingNames]
            # output to file
            write_csv(outputFile,wrestler)

        start = start + 100


    
       