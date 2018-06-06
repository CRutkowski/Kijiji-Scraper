#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

import datetime
import time
import sys
import os

skip_flag = False

def ParseAd(html):  # Parses ad html trees and sorts relevant data into a dictionary
    ad_info = {}
    
    #description = html.find('div', {"class": "description"}).text.strip()
    #description = description.replace(html.find('div', {"class": "details"}).text.strip(), '')
    #print(description)
    try:
        ad_info["Title"] = html.find('a', {"class": "title"}).text.strip()
    except:
        print('[Error] Unable to parse Title data.')
        
    try:
        ad_info["Image"] = str(html.find('img'))
    except:
        print('[Error] Unable to parse Image data')

    try:
        ad_info["Url"] = 'http://www.kijiji.ca' + html.get("data-vip-url")
    except:
        print('[Error] Unable to parse URL data.')
        
    try:
        ad_info["Details"] = html.find('div', {"class": "details"}).text.strip()
    except:
        print('[Error] Unable to parse Details data.')   
        
    try:
        description = html.find('div', {"class": "description"}).text.strip()
        description = description.replace(ad_info["Details"], '')
        ad_info["Description"] = description
    except:
        print('[Error] Unable to parse Description data.')    

    try:
        ad_info["Date"] = html.find('span', {"class": "date-posted"}).text.strip()
    except:
        print('[Error] Unable to parse Date data.')    
    
    try:
        location = html.find('div', {"class": "location"}).text.strip()
        location = location.replace(ad_info["Date"], '')        
        ad_info["Location"] = location
    except:
        print('[Error] Unable to parse Location data.')

    try:
        ad_info["Price"] = html.find('div', {"class": "price"}).text.strip()
    except:
        print('[Error] Unable to parse Price data.')

    return ad_info


def WriteAds(ad_dict, filename):  # Writes ads from given dictionary to given file
    try:
        file = open(filename, 'a')
        for ad_id in ad_dict:
            file.write(ad_id)
            file.write(str(ad_dict[ad_id]) + "\n")
        file.close()
    except:
        print('[Error] Unable to write ad(s) to file.')


def ReadAds(filename):  # Reads given file and creates a dict of ads in file
    import ast
    if not os.path.exists(filename):  # If the file doesn't exist, it makes it.
        file = open(filename, 'w')
        file.close()

    ad_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() != '':
                index = line.find('{')
                ad_id = line[:index]
                dictionary = line[index:]
                dictionary = ast.literal_eval(dictionary)
                ad_dict[ad_id] = dictionary
    return ad_dict


def MailAd(ad_dict, email_title):  # Sends an email with a link and info of new ads
    import smtplib
    from email.mime.text import MIMEText

    
    # Fill in the variables below with your info
    #------------------------------------------
    sender = 'sender@example.com'
    passwd = 'Sender Password'
    receiver = 'receiver@example.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    #------------------------------------------

    count = len(ad_dict)
    if count > 1:
        subject = str(count) + ' New ' + email_title + ' Ads Found!'
    if count == 1:
        subject = 'One New ' + email_title + ' Ad Found!'

    body = '<!DOCTYPE html> \n<html> \n<body>'
    try:
        for ad_id in ad_dict:
            body += '<p><b>' + ad_dict[ad_id]['Title'] + '</b>' + ' - ' + ad_dict[ad_id]['Location']
            body += ' - ' + ad_dict[ad_id]['Date'] + '<br /></p>'
            body += '<a href="' + ad_dict[ad_id]['Url'] + '">'
            body += ad_dict[ad_id]['Image'] + '</a>'
            body += '<p>' + ad_dict[ad_id]['Description'] + '<br />'
            if ad_dict[ad_id]['Details'] != '':
                body += ad_dict[ad_id]['Details'] + '<br />' + ad_dict[ad_id]['Price'] + '<br /><br /><br /><br /></p>'
            else:
                body += ad_dict[ad_id]['Price'] + '<br /><br /><br /><br /></p>'
    except:
        body +='<p>' +  ad_dict[ad_id]['Title'] + '<br />'
        body += ad_dict[ad_id]['Url'] + '<br /><br />' + '</p>'
        print('[Error] Unable to create body for email message')

    body += '<p>This is an automated message, please do not reply to this message.</p>'
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
    except:
        print('[Error] Unable to connect to email server.')
    try:
        server.login(sender, passwd)
    except:
        print('[Error] Unable to login to email server.')
    try:
        server.send_message(msg)
        server.quit()
        print('[Okay] Email message successfully delivered.')
    except:
        print('[Error] Unable to send message.')


def scrape(url, old_ad_dict, exclude_list, filename):  # Pulls page data from a given kijiji url and finds all ads on each page
    # Initialize variables for loop
    email_title = None
    ad_dict = {}
    third_party_ad_ids = []
    
    while url: 
    
        try:
            page = requests.get(url) # Get the html data from the URL
        except:
            print("[Error] Unable to load " + url)
            sys.exit(1)
    
        soup = BeautifulSoup(page.content, "html.parser")
        
        if not email_title: # If the email title doesnt exist pull it form the html data
            email_title = soup.find('div', {'class': 'message'}).find('strong').text.strip('"')
            email_title = toUpper(email_title)
            
        kijiji_ads = soup.find_all("div", {"class": "regular-ad"})  # Finds all ad trees in page html.
        
        third_party_ads = soup.find_all("div", {"class": "third-party"}) # Find all third-party ads to skip them
        for ad in third_party_ads:
            third_party_ad_ids.append(ad['data-ad-id'])
            
    
        exclude_list = toLower(exclude_list) # Make all words in the exclude list lower-case
        #checklist = ['miata']
        for ad in kijiji_ads:  # Creates a dictionary of all ads with ad id being the keys.
            title = ad.find('a', {"class": "title"}).text.strip() # Get the ad title
            ad_id = ad['data-ad-id'] # Get the ad id
            if not [False for match in exclude_list if match in title.lower()]: # If any of the title words match the exclude list then skip
                #if [True for match in checklist if match in title.lower()]:
                if (ad_id not in old_ad_dict and ad_id not in third_party_ad_ids): # Skip third-party ads and ads already found
                    print('[Okay] New ad found! Ad id: ' + ad_id)
                    ad_dict[ad_id] = ParseAd(ad) # Parse data from ad
        url = soup.find('a', {'title' : 'Next'})
        if url:
            url = 'https://www.kijiji.ca' + url['href']

    if ad_dict != {}:  # If dict not emtpy, write ads to text file and send email.
        WriteAds(ad_dict, filename) # Save ads to file
        if not skip_flag: # if skip flag is set do not send out email
            MailAd(ad_dict, email_title) # Send out email with new ads
            
def toLower(input_list): # Rturns a given list of words to lower-case words
    output_list = list()
    for word in input_list:
        output_list.append(word.lower())
    return output_list

def toUpper(title): # Makes the first letter of every word upper-case
    new_title = list()
    title = title.split()
    for word in title:
        new_word = ''
        new_word += word[0].upper()
        if len(word) > 1:
            new_word += word[1:]
        new_title.append(new_word)
    return ' '.join(new_title)

def main(): # Main function, handles command line arguments and calls other functions for parsing ads
    args = sys.argv
    if args[1] == '-h' or args[1] == '--help': # Print script usage help
        print('Usage: Kijiji-Scraper.py URL [-f] [-e] [-s]\n')
        print('Positional arguments:')
        print(' URL\t\tUrl to scrape for ads\n')
        print('Optional arguments:')
        print(' -h, --help  show this help message and exit')
        print(' -f\t\tfilename to store ads in (default name is the url)')
        print(' -e\t\tword that will exclude an ad if its in the title (can be a single word or multiple words seperated by spaces')
        print(' -s\t\tflag that causes the program to skip sending an email. Useful if you want to index ads but not be notified of them')
    else:
        url_to_scrape = args[1]
        if '-f' in args:
            filename = args.pop(args.index('-f') + 1)
            filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
            args.remove('-f')
        else:
            filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), url_to_scrape)
        if '-s' in args:
            skip_flag = True
            args.remove('-s')
        if '-e' in args:
            exclude_list = args[args.index('-e') + 1:]
        else:
            exclude_list = list()
        
    old_ad_dict = ReadAds(filename)
    print("[Okay] Ad database succesfully loaded.")
    scrape(url_to_scrape, old_ad_dict, exclude_list, filename)

if __name__ == "__main__":
    main()
