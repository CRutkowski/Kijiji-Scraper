# Kijiji-Scraper
Python script that scrapes Kijiji ad information and sends out an email
when a new ad is found.
It's designed to be run in the background (Pythonw).

Dependencies: requests and BeautifulSoup

To configure the script:
-Set the 'url_to_scrape' variable to the url of the Kijiji ad page you want to scrape.
    e.g. 'http://www.kijiji.ca/b-cars-trucks/calgary/convertible__coupe__hatchback__other+body+type__sedan__wagon-mazda-mx5miata/c174l1700199a138a54a1000054'
    
-Set the 'scrape_delay' variable to them time in seconds before re-scraping. (default = 600)

-Replace SENDER_EMAIL, SENDER_EMAIL_PASSWORD, RECEIVER_EMAIL fields in the 'MailAd' with your email info.