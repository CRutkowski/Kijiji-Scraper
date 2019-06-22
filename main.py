import config
from kijiji_scraper.kijiji_scraper import KijijiScraper
from kijiji_scraper.email_client import EmailClient
import sys

if __name__ == "__main__":
    args = sys.argv
    skip_flag = "-s" in args

    # Initialize the KijijiScraper and email client
    kijiji_scraper = KijijiScraper()
    email_client = EmailClient()

    # Scrape each url given in config file
    for url_dict in config.urls_to_scrape:
        url = url_dict.get("url")
        exclude_words = url_dict.get("exclude_words", [])

        kijiji_scraper.set_exclude_list(exclude_words)
        ads, email_title = kijiji_scraper.scrape_kijiji_for_ads(url)

        if not skip_flag and len(ads):
            email_client.mail_ads(ads, email_title)

    kijiji_scraper.save_ads()
