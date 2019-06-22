#!/usr/bin/env python3
import yaml
import sys

from kijiji_scraper.kijiji_scraper import KijijiScraper
from kijiji_scraper.email_client import EmailClient

if __name__ == "__main__":
    args = sys.argv
    skip_flag = "-s" in args

    # Get config values
    with open("config.yaml", "r") as config_file:
        email_config, urls_to_scrape = yaml.safe_load_all(config_file)

    # Initialize the KijijiScraper and email client
    kijiji_scraper = KijijiScraper()
    email_client = EmailClient(email_config)

    # Scrape each url given in config file
    for url_dict in urls_to_scrape:
        url = url_dict.get("url")
        exclude_words = url_dict.get("exclude", [])

        print(f"Scraping: {url}")
        if len(exclude_words):
            print("Excluding: " + ", ".join(exclude_words))

        kijiji_scraper.set_exclude_list(exclude_words)
        ads, email_title = kijiji_scraper.scrape_kijiji_for_ads(url)

        info_string = f"Found {len(ads)} new ads\n" \
            if len(ads) != 1 else "Found 1 new ad\n"
        print(info_string)

        if not skip_flag and len(ads):
            email_client.mail_ads(ads, email_title)

    kijiji_scraper.save_ads()
