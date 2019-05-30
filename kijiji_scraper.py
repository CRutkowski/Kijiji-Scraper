import requests
from bs4 import BeautifulSoup
import json
import os


class KijijiScraper():

    def __init__(self, filename="ads.json"):
        self.filename = filename
        self.all_ads = {}
        self.new_ads = {}

        self.third_party_ads = []
        self.exclude_list = []

        self.load_ads()

    # Reads given file and creates a dict of ads in file
    def load_ads(self):
        # If the file doesn't exist create it
        if not os.path.exists(self.filename):
            ads_file = open(self.filename, 'w')
            ads_file.write("{}")
            ads_file.close()
            return

        with open(self.filename, "r") as ads_file:
            self.all_ads = json.load(ads_file)

    # Save ads to file
    def save_ads(self):
        with open(self.filename, "w") as ads_file:
            json.dump(self.all_ads, ads_file)

    # Set exclude list
    def set_exclude_list(self, exclude_words):
        self.exclude_list = self.words_to_lower(exclude_words)

    # Pulls page data from a given kijiji url and finds all ads on each page
    def scrape_kijiji_for_ads(self, url):
        self.new_ads = {}

        email_title = None
        while url:
            # Get the html data from the URL
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            # If the email title doesnt exist pull it from the html data
            if email_title is None:
                email_title = self.get_email_title(soup)

            # Find ads on the page
            self.find_ads(soup)

            # Set url for next page of ads
            url = soup.find('a', {'title': 'Next'})
            if url:
                url = 'https://www.kijiji.ca' + url['href']

        return self.new_ads, email_title

    def get_email_title(self, soup):
        email_title_location = soup.find('div', {'class': 'message'})

        if email_title_location:

            if email_title_location.find('strong'):
                email_title = email_title_location.find('strong')\
                    .text.strip('"').strip(" »").strip("« ")
                return self.format_title(email_title)

        content = soup.find_all('div', class_='content')
        for i in content:

            if i.find('strong'):
                email_title = i.find('strong')\
                    .text.strip(' »').strip('« ').strip('"')
                return self.format_title(email_title)

        return ""

    def find_ads(self, soup):
        # Finds all ad trees in page html.
        kijiji_ads = soup.find_all("div", {"class": "regular-ad"})

        # Find all third-party ads to skip them
        third_party_ads = soup.find_all("div", {"class": "third-party"})
        for ad in third_party_ads:
            self.third_party_ads.append(ad['data-ad-id'])

        # Create a dictionary of all ads with ad id being the key
        for ad in kijiji_ads:
            title = ad.find('a', {"class": "title"}).text.strip()
            ad_id = ad['data-ad-id']

            # If any of the title words match the exclude list then skip
            if not [False for match in self.exclude_list
                    if match in title.lower()]:

                # Skip third-party ads and ads already found
                if (ad_id not in self.all_ads and
                        ad_id not in self.third_party_ads):

                    print("Found new ad: " + str(ad_id))

                    parsed_ad = self.parse_ad(ad)
                    self.new_ads[ad_id] = parsed_ad
                    self.all_ads[ad_id] = parsed_ad

    def parse_ad(self, ad):
        ad_info = {}

        # Locate ad information
        ad_info["Title"] = ad.find('a', {"class": "title"})
        ad_info["Image"] = str(ad.find('img'))
        ad_info["Url"] = ad.get("data-vip-url")
        ad_info["Details"] = ad.find('div', {"class": "details"}).text.strip()
        ad_info["Description"] = ad.find('div', {"class": "description"})
        ad_info["Date"] = ad.find('span', {"class": "date-posted"})\
            .text.strip()
        ad_info["Location"] = ad.find('div', {"class": "location"})
        ad_info["Price"] = ad.find('div', {"class": "price"})

        # Parse ad information
        for key, value in ad_info.items():
            if value:
                if key == "Url":
                    ad_info[key] = 'http://www.kijiji.ca' + value

                elif key == "Description":
                    ad_info[key] = value.text.strip()\
                        .replace(ad_info["Details"], '')

                elif key == "Location":
                    ad_info[key] = value.text.strip()\
                        .replace(ad_info["Date"], '')

                elif key not in ["Image", "Details", "Date"]:
                    ad_info[key] = value.text.strip()

        return ad_info

    # Makes the first letter of every word upper-case
    def format_title(self, title):
        new_title = []

        title = title.split()
        for word in title:
            new_word = ''
            new_word += word[0].upper()

            if len(word) > 1:
                new_word += word[1:]

            new_title.append(new_word)

        return ' '.join(new_title)

    # Returns a given list of words to lower-case words
    def words_to_lower(self, words):
        return [word.lower() for word in words]
