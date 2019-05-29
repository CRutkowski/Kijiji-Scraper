import config
from kijiji_scraper import KijijiScraper
import sys

if __name__ == "__main__":
    args = sys.argv
    skip_flag = "-s" in args

    # Initialize the KijijiScraper object
    kijiji_scraper = KijijiScraper(skip_flag=skip_flag)

    # Scrape each url given in config file
    for url_dict in config.urls_to_scrape:
        url = url_dict.get("url")
        exclude_words = url_dict.get("exclude_words", [])

        kijiji_scraper.set_exclude_list(exclude_words)
        kijiji_scraper.scrape_kijiji_for_ads(url)

    kijiji_scraper.save_ads()
