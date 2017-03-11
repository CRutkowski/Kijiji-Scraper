#!C:\Python34\scrapper\Scripts

# Place url, linking to ad list, with desired search filters here.
url_to_scrape = "http://www.kijiji.ca/b-canot-kayak-paddle-board/quebec/kayak/k0c329l9001"

# Set the delay in (s) that the programs waits before scraping again.
scrape_delay = 600  # 600 = 10 mins

# Set filename to store ads in.
filename = 'ads.txt'

import requests
from bs4 import BeautifulSoup

import datetime
import time


def ParseAd(html):  # Parses ad html trees and sorts relevant data into a dictionary
    ad_info = {}
    try:
        ad_info["Title"] = html.find_all('a', {"class": "title"})[0].text.strip()
    except:
        log('[Error] Unable to parse Title data.')

    try:
        ad_info["Url"] = 'http://www.kijiji.ca' + html.get("data-vip-url")
    except:
        log('[Error] Unable to parse URL data.')

    try:
        ad_info["Description"] = html.find_all('div', {"class": "description"})[0].text.strip()
    except:
        log('[Error] Unable to parse Description data.')

    try:
        tempsoup = html.find_all('div', {"class": "location"})[0].text.strip()
        if tempsoup.find('-') > 0:
            tempsoup = tempsoup[:tempsoup.find('-') - 2]
        ad_info["Location"] = tempsoup
    except:
        log('[Error] Unable to parse Location data.')

    try:
        ad_info["Date"] = html.find_all('span', {"class": "date-posted"})[0].text.strip()
    except:
        log('[Error] Unable to parse Date data.')

    try:
        ad_info["Price"] = html.find_all('div', {"class": "price"})[0].text.strip()
    except:
        log('[Error] Unable to parse Price data.')

    return ad_info


def WriteAds(ad_dict, filename):  # Writes ads to given file
    try:
        file = open(filename, 'a')
        for ad_id in ad_dict:
            file.write(ad_id)
            file.write(str(ad_dict[ad_id]) + "\n")
            log('[Okay] Ad ' + ad_id + ' written to database.')
        file.close()
    except:
        log('[Error] Unable to write ad(s) to database.')


def ReadAds(filename):  # Reads given file and creates a dict of ads in file
    import ast
    import os.path
    if not os.path.isfile(filename):  # If the file doesn't exist, it makes it.
        file = open(filename, 'w')
        file.close()

    ad_dict = {}
    file = open(filename, 'r')
    for line in file:
        if line.strip() != '':
            index = line.find('{')
            ad_id = line[:index]
            dictionary = line[index:]
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
    file.close()
    return ad_dict


def log(text):  # writes log data to log.txt with datetime.
    date_time = datetime.datetime.now()
    myfile = open('log.txt', 'a')
    date_time = str(date_time) + '\n'
    text += '\n\n'
    myfile.write(date_time)
    myfile.write(text)
    myfile.close()


def MailAd(ad_dict):  # Sends an email with a link and info of new ads
    import smtplib
    from email.mime.text import MIMEText

    sender = 'email@example.com'
    passwd = 'Password'
    receiver = 'email@example.com'

    count = len(ad_dict)
    if count > 1:
        subject = str(count) + ' Nouvelle annonces trouvés!'
    if count == 1:
        subject = 'Une nouvelle annonce trouvé'

    body = ''
    try:
        for ad_id in ad_dict:
            body += ad_dict[ad_id]['Title'] + ' - ' + ad_dict[ad_id]['Price'] + ' - ' + ad_dict[ad_id]['Location']
            body += ' - ' + ad_dict[ad_id]['Date'] + '\n'
            body += ad_dict[ad_id]['Url'] + '\n\n'

    except:
        log('[Error] Unable to create body for email message')

    body += 'This is an automated message.\nPlease do not reply to this message.'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        server = smtplib.SMTP('smtp.live.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
    except:
        log('[Error] Unable to connect to email server.')
    try:
        server.login(sender, passwd)
    except:
        log('[Error] Unable to login to email server.')
    try:
        server.send_message(msg)
        server.quit()
        log('[Okay] Email message successfully delivered.')
    except:
        log('[Error] Unable to send message.')


def main(old_ad_dict):  # Main function, brings it all together.
    try:
        page = requests.get(url_to_scrape)
        log("[Okay] Retrieved HTML data from: " + url_to_scrape)
    except:
        log("[Error] Unable to load html data from: " + url_to_scrape)

    soup = BeautifulSoup(page.content, "html.parser")
    page = None

    kijiji_ads = soup.find_all("div", {"class": "regular-ad"})  # Finds all ad trees in page html.

    ad_dict = {}
    checklist = ['boréal', 'kayak de mer', 'baffin', 'epsilon', 'scorpio']
    excludelist = ['wanted', 'recherché']
    for ad in kijiji_ads:  # Creats a dictionary of all ads sorted by ad id.
        title = ad.find_all('a', {"class": "title"})[0].text.strip()
        ad_id = ad.find_all('div', {'class': "watch"})[0].get('data-adid')
        if not [False for match in excludelist if match in title.lower()]:
            if [True for match in checklist if match in title.lower()]:
                if ad_id not in old_ad_dict:
                    log('[Okay] New ad found! Ad id: ' + ad_id)
                    ad_dict[ad_id] = ParseAd(ad)

    if ad_dict != {}:  # If dict not emtpy, write ads to text file and send email.
        WriteAds(ad_dict, filename)
        MailAd(ad_dict)
        try:
            old_ad_dict = ReadAds(filename)
            log("[Okay] Database succesfully reloaded.")
        except:
            log("[Error] Unable to reload database.")
    time.sleep(scrape_delay)
    main(old_ad_dict)


if __name__ == "__main__":
    old_ad_dict = ReadAds(filename)
    log("[Okay] Ad database succesfully loaded.")
    myfile = open('log.txt', 'w')  # Create/Empty log file
    myfile.close()
    main(old_ad_dict)
