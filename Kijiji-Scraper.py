#!/usr/bin/env python3


# Place url, linking to ad list, with desired search filters here.
# e.g. http://www.kijiji.ca/b-cars-trucks/calgary/convertible__coupe__hatchback__other+body+type__sedan__wagon-mazda-mx5miata/c174l1700199a138a54a1000054
url_to_scrape = ""

# Set the delay in (s) that the programs waits before scraping again.
scrape_delay = 600 # 600 = 10 mins

# Set filename to store ads in.
filename = 'ads.txt'

import requests
from bs4 import BeautifulSoup
import datetime
import time


def ParseAd(html): # Parses ad html trees and sorts relevant data into a dictionary
   ad_info = {}
   try:
      ad_info["Url"] = 'http://www.kijiji.ca' + html.get("data-vip-url")
   except:
      log('[Error] Unable to parse URL data.')
      
   try:
      ad_info["Title"] = html.find_all('a',{"class":"title"})[0].text.strip()
   except:
      log('[Error] Unable to parse Title data.')
            
   try:
      description,details = html.find_all('p')
      ad_info["Description"] = description = description.text.strip()
   except:
      log('[Error] Unable to parse Description data.')
         
   try:
      checklist = ['Automatic','Manual','Other']
      details = details.text.split('|')
      for item in details:
         if item == '\n':
            pass
         if 'km' in item:
            ad_info["Mileage"] = item.strip()
         if item.strip() in checklist:
            ad_info["Trans"] = item.strip()
   except:
      log('[Error] Unable to parse Mileage/Trans data.')      
      
   try:
      ad_info["Date"] = html.find_all('td',{"class":"posted"})[0].text.strip()
   except:
      log('[Error] Unable to parse Date data.')      
      
   try:
      ad_info["Price"] = html.find_all('td',{"class":"price"})[0].text.strip()
   except:
      log('[Error] Unable to parse Price data.')
         
   return ad_info

def WriteAds(ad_dict,filename): # Writes ads to given file
   try:
      file = open(filename,'a')
      for ad_id in ad_dict:
         file.write(ad_id)
         file.write(str(ad_dict[ad_id]) + "\n")
         log('[Okay] Ad ' + ad_id + ' written to database.')
      file.close()
   except:
      log('[Error] Unable to write ad(s) to database.')

def ReadAds(filename): # Reads given file and creates a dict of ads in file
   import ast
   import os.path
   if not os.path.isfile(filename): # If the file doesn't exist, it makes it.
      file = open(filename,'w')
      file.close()   

   ad_dict = {}
   file = open(filename,'r')
   for line in file:
      if line.strip() != '':
         index = line.find('{')
         ad_id = line[:index]
         dictionary = line[index:]
         dictionary = ast.literal_eval(dictionary)
         ad_dict[ad_id] = dictionary
   file.close()
   return ad_dict

def log(text): # writes log data to log.txt with datetime.
   date_time = datetime.datetime.now()
   file = open('log.txt','a')
   date_time = str(date_time) + '\n'
   text = text + '\n\n'
   file.write(date_time)
   file.write(text)
   file.close()
   
def MailAd(ad_dict): # Sends an email with a link and info of new ads
   import smtplib
   from email.mime.text import MIMEText
   
   sender = 'SENDER_EMAIL'
   passwd = 'SENDER_EMAIL_PASSWORD'
   receiver = 'RECEIVER_EMAIL'
   
   count = len(ad_dict)
   if count > 1:
      subject = str(count) + ' New Ads Found!'
   if count == 1:
      subject = '1 New Ad Found!'
   
   body = ''
   try:
      for ad_id in ad_dict:
         body = body + ad_dict[ad_id]['Title'] + '\n'
         body = body + ad_dict[ad_id]['Url'] + '\n\n'
         body = body + ad_dict[ad_id]['Description'] + '\n\n'
         if 'Mileage' in ad_dict[ad_id]:
            body = body + ad_dict[ad_id]['Mileage'] + '\t\t' + ad_dict[ad_id]['Trans'] + '\n'
         if 'Price' in ad_dict[ad_id]:
            body = body + ad_dict[ad_id]['Price']
         body = body + '\n\n\n'
      body = body +  'This is an automated message.\nPlease do not reply to this message.'
   except:
      log('[Error] Unable to create body for email message')
      
   msg = MIMEText(body)
   msg['Subject'] = subject
   msg['From'] = sender
   msg['To'] = receiver
   
   try:
      server = smtplib.SMTP('smtp.gmail.com', 587)
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
   
def main(old_ad_dict): # Main function, brings it all together.
   try:
      page = requests.get(url_to_scrape)
      log("[Okay] Retrieved HTML data from: " + url_to_scrape)
   except:
      log("[Error] Unable to load html data from: " + url_to_scrape)
   soup = BeautifulSoup(page.content,"html.parser")
   page = None

   kijiji_ads = soup.find_all("table",{"class":"regular-ad"}) # Finds all ad trees in page html.

   ad_dict = {}
   
   for ad in kijiji_ads: # Creats a dictionary of all ads sorted by ad id.
      title  = ad.find_all('a',{"class":"title"})[0].text.strip()[0:6]
      ad_id = ad.find_all('div',{'class':"watch"})[0].get('data-adid')
      if not title == "Wanted": # Checks and skips any ad that's "Wanted".
         if ad_id not in old_ad_dict:
            log('[Okay] New ad found! Ad id: '+ ad_id)
            ad_dict[ad_id] = ParseAd(ad)
               
   if ad_dict != {}: # If dict not emtpy, write ads to text file and send email.
      WriteAds(ad_dict,filename)
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
   file = open('log.txt','w') # Create/Empty log file
   file.close()   
   main(old_ad_dict)