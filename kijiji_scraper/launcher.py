import yaml
import sys
import os
import argparse
from shutil import which

from kijiji_scraper.kijiji_scraper import KijijiScraper
from kijiji_scraper.email_client import EmailClient
from . import VERSION

def parse_args():
    parser = argparse.ArgumentParser(description="""Kijiji scraper: Track ad informations and sends out an email when a new ads are found""")
    parser.add_argument('--init', help="Create config file and open with default text editor", action='store_true')
    parser.add_argument('--conf', '-c', metavar='File path', help="""The script * must read a configuration file to set mail server settings *. Default config file config.yalm is located in ~/.kijiji_scraper/ (MacOS/Linux), APPDATA/.kijiji_scraper (Windows) or directly in the install folder.""")
    parser.add_argument('--url', '-u', metavar="URL", help="Kijiji seacrh URLs to scrape", nargs='+', default=None)
    parser.add_argument('--email','-e', metavar="Email", help="Email recepients", nargs='+',  default=None)
    parser.add_argument('--skipmail', '-s', help="Do not send emails. This is useful for the first time you scrape a Kijiji as the current ads will be indexed and after removing the flag you will only be sent new ads.", action='store_true')
    parser.add_argument('--all', '-a', help="Reconsider all ads, just for this run", action='store_true')
    parser.add_argument('--version', '-V', help="Print Kijiji-Scraper version", action='store_true')
    args = parser.parse_args()
    return(args)

def main():
    # parse the arguments 
    args = parse_args()

    if args.version:
        print("Version:\t\t%s" %VERSION)
        exit(0)

    if args.init:
        init()
        exit(0)
    
    # Handle custom config file
    if args.conf:
        filepath=args.conf
    else:
        filename=".kijiji_scraper/config.yaml"
        # Find the default config file from env varibles
        filepath = find_file(['HOME', 'XDG_CONFIG_HOME', 'APPDATA'], [filename])
        if not filepath:
            # Find the default config file in the install directory
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(os.path.dirname(abspath))
            filepath=os.path.join(dname, "config.yaml")
            if not os.path.exists(filepath):
                filepath=None
    if filepath:
        # Get config values
        with open(filepath, "r") as config_file:
            email_config, urls_to_scrape = yaml.safe_load_all(config_file)
        print("Loaded config file: %s"%filepath)
    else:
        print("No config file loaded")
        email_config, urls_to_scrape = ({},{})
        # Do not try to send mail if no config file is loaded
        args.skipmail=True
    print()

    # Initialize the KijijiScraper and email client
    filepath = find_file(['HOME', 'XDG_CONFIG_HOME', 'APPDATA'], ['.kijiji_scraper/ads.json'], default_content='{}', create=True) if not args.all else None
    kijiji_scraper = KijijiScraper(filepath)
   
    # Overwrite search URLs if specified
    if args.url: urls_to_scrape = [{'url':u} for u in args.url]

    # Scrape each url given in config file
    for url_dict in urls_to_scrape:
        url = url_dict.get("url")
        exclude_words = url_dict.get("exclude", [])

        print("Scraping: %s"%url)
        if len(exclude_words):
            print("Excluding: " + ", ".join(exclude_words))

        kijiji_scraper.set_exclude_list(exclude_words)
        ads, email_title = kijiji_scraper.scrape_kijiji_for_ads(url)

        info_string = "Found %s new ads"%len(ads) \
            if len(ads) != 1 else "Found 1 new ad"
        print(info_string)
        print(get_ads_summary(ads))

        if not args.skipmail and len(ads):
            email_client = EmailClient(email_config)
            # Overwrite email recepeients if specified
            if args.email: email_client.receiver=','.join(args.email)
            email_client.mail_ads(ads, email_title)

    kijiji_scraper.save_ads()

def get_ads_summary(ads):
    string=''
    if not ads: return string
    header = ("Title", "Url")
    title_w=20
    # Determine the longest width for Title column
    for ad_id in ads:
        title_w=len(ads[ad_id]['Title'])+4 if ads[ad_id] and len(ads[ad_id]['Title'])>title_w else title_w
    frow="{:<%d} {}"%title_w
    string+=frow.format(*header)

    for ad_id in ads:
        string+='\n'
        string+=frow.format(str(ads[ad_id]['Title']), str(ads[ad_id]['Url']))

    return string

def find_file(env_location, potential_files, default_content="", create=False):
    potential_paths=[]
    existent_file=None
    # build potential_paths of config file
    for env_var in env_location:
        if env_var in os.environ:
            for file_path in potential_files:
                potential_paths.append(os.path.join(os.environ[env_var],file_path))
    # If file exist, add to list
    for p in potential_paths:
        if os.path.isfile(p):
            existent_file=p
            break
    # If no file foud and create=True, init new template config
    if existent_file==None and create:
        os.makedirs(os.path.dirname(potential_paths[0]), exist_ok=True)
        with open(potential_paths[0],'w') as config_file:
            config_file.write(default_content)
        print("Init new file: %s"%(p))
        existent_file=potential_paths[0]

    return(existent_file)

def init():
    default_config="""
# Replace the values in the fields below with your own info so the scraper can send out emails.

# "sender" is the email address that will be sending out the emails. I made a throwaway gmail account for this.
# "password" is the password for the sender account.
# "receiver" is the email address that the sender email account will be sending the email to.
# "smtp server" is the smtp server the sender email account uses. If the sender email is a gmail address you do not need to change this.
# "smtp port" is the port the above smtp server uses. If the sender email is a gmail address you do not need to change this.

from: sender@example.com
username: sender@example.com
password: Sender Password
receiver: receiver@example.com
smtp server: smtp.gmail.com
smtp port: 465

---
# Set the URLs you wish to scrape below with an optional list of words to exclude per URL.
# Any filters you apply on the Kijij website are a part of the URL and will apply to the scraper.
# "url" is as you would guess the URL you want to scrape.
# "exclude" is a list of words, if an ad title contains any one of the words it will be ignored. Add as many words as you desire.

# There are a couple examples below which you will want to remove/replace with your own.
# You can add as many URLs as you wish to scrape.

# Just a URL to scrape
- url: https://www.kijiji.ca/b-bikes/alberta/kona-stinky/k0c644l9003?price=__700

# Url with exclude words given
- url: https://www.kijiji.ca/b-cars-trucks/alberta/tesla-new__used/c174l9003a54a49
  exclude:
    - wanted
    - gas
    - base
"""
    # Find file or create it
    filepath=find_file(['HOME', 'XDG_CONFIG_HOME', 'APPDATA'], [".kijiji_scraper/config.yaml"], default_content=default_config, create=True)
    # Open with editor
    if os.name == 'nt':
        os.system(filepath)
    elif 'EDITOR' in os.environ:
        os.system('%s %s' % (os.getenv('EDITOR'), filepath))
    elif which('gedit') is not None:
        os.system('gedit %s'%filepath)
    elif which('nano') is not None:
        os.system('nano %s'%filepath)
    elif which('vim') is not None:
        os.system('vim %s'%filepath)
