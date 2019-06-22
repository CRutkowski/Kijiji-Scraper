import requests
from bs4 import BeautifulSoup
import json
from kijiji_scraper.kijiji_ad import KijijiAd
from pathlib import Path


class KijijiScraper():

    def __init__(self, filename="ads.json"):
        self.filepath = Path().absolute().joinpath(filename)
        self.all_ads = {}
        self.new_ads = {}

        self.third_party_ads = []
        self.exclude_list = []

        self.load_ads()

    # Reads given file and creates a dict of ads in file
    def load_ads(self):
        # If the file doesn't exist create it
        if not self.filepath.exists():
            ads_file = self.filepath.open(mode='w')
            ads_file.write("{}")
            ads_file.close()
            return

        with self.filepath.open(mode="r") as ads_file:
            self.all_ads = json.load(ads_file)

    # Save ads to file
    def save_ads(self):
        with self.filepath.open(mode="w") as ads_file:
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
        kijiji_ads = soup.find_all("div", {"class": "search-item regular-ad"})

        # Find all third-party ads to skip them
        third_party_ads = soup.find_all("div", {"class": "third-party"})
        for ad in third_party_ads:
            thid_party_ad_id = KijijiAd(ad).id
            self.third_party_ads.append(thid_party_ad_id)

        # Create a dictionary of all ads with ad id being the key
        for ad in kijiji_ads:
            kijiji_ad = KijijiAd(ad)

            # If any of the title words match the exclude list then skip
            if not [False for match in self.exclude_list
                    if match in kijiji_ad.title.lower()]:

                # Skip third-party ads and ads already found
                if (kijiji_ad.id not in self.all_ads and
                        kijiji_ad.id not in self.third_party_ads):

                    print("Found new ad: " + str(kijiji_ad.id))

                    self.new_ads[kijiji_ad.id] = kijiji_ad.info
                    self.all_ads[kijiji_ad.id] = kijiji_ad.info

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
