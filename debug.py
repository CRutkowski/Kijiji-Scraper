#utf-8

import requests
from bs4 import BeautifulSoup
import datetime
import time

url_to_scrape = "http://www.kijiji.ca/b-canot-kayak-paddle-board/quebec/kayak/k0c329l9001"

try:
    page = requests.get(url_to_scrape)
    print("[Okay] Retrieved HTML data from: " + url_to_scrape)
except:
    print("[Error] Unable to load html data from: " + url_to_scrape)


soup = BeautifulSoup(page.content, "html.parser")

kijiji_ads = soup.find_all("div", {"class": "regular-ad"})  # Finds all ad trees in page html.

page = None

kijiji_ads = soup.find_all("div", {"class": "regular-ad"})  # Finds all ad trees in page html.

ad_dict = {}


def parse_ad(html):  # Parses ad html trees and sorts relevant data into a dictionary
    ad_info = {}
    try:
        ad_info["Url"] = 'http://www.kijiji.ca' + html.get("data-vip-url")
    except:
        print('[Error] Unable to parse URL data.')

    try:
        ad_info["Title"] = html.find_all('a', {"class": "title"})[0].text.strip()
    except:
        print('[Error] Unable to parse Title data.')

    try:
        ad_info["Description"] = html.find_all('div', {"class": "description"})[0].text.strip()
    except:
        print('[Error] Unable to parse Description data.')

    try:
        tempsoup = html.find_all('div', {"class": "location"})[0].text.strip()
        if tempsoup.find('-') > 0:
            tempsoup = tempsoup[:tempsoup.find('-')-2]
        ad_info["Location"] = tempsoup
    except:
        print('[Error] Unable to parse Location data.')

    try:
        ad_info["Date"] = html.find_all('span', {"class": "date-posted"})[0].text.strip()
    except:
        print('[Error] Unable to parse Date data.')

    try:
        ad_info["Price"] = html.find_all('div', {"class": "price"})[0].text.strip()
    except:
        print('[Error] Unable to parse Price data.')
    print(ad_info)

    #checklist = ['Boréal', 'Kayak de mer']

for ad in kijiji_ads:  # Creats a dictionary of all ads sorted by ad id.
    title1 = ad.find_all('a', {"class": "title"})[0].text.strip()
    checklist = ['boréal', 'kayak de mer']
    if [True for match in checklist if match in title1.lower()]:
        print('Match!<---------------------------')


    print(title1)
    title = ad.find_all('a', {"class": "title"})[0].text.strip()[0:6]
    ad_id = ad.find_all('div', {'class': "watch"})[0].get('data-adid')
    if not title == "Wanted":  # Checks and skips any ad that's "Wanted".
        print('[Okay] New ad found! Ad id: ' + ad_id)
        parse_ad(ad)


