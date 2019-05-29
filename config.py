# Config file for the Kijiji scraper

# Config values for email client
sender = 'sender@example.com'
passwd = 'Sender Password'
receiver = 'receiver@example.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 465

# Urls to scrape with an optional list of words to exclude per ad
urls_to_scrape = [
    {
        "url": "https://www.kijiji.ca/b-alberta/canoe/k0l9003?price=100__300",
        "exclude_words": ["wanted", "sunk"]
    },

    {
        "url": "https://www.kijiji.ca/b-alberta/paddle-board/k0l9003?price=2000__"
    }
]
