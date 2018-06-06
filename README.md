# Kijiji-Scraper 2.5
## Python script that scrapes Kijiji ad information and sends out an email when a new ad is found.


 **Replace SENDER_EMAIL, SENDER_EMAIL_PASSWORD, RECEIVER_EMAIL fields in the 'MailAd' function with your email info.**
 
 - If you're using gmail, you'll have to go to 'My Account>Sign in & security>Connected apps & sites' then turn "Allow less secure apps" to "On".
 
 **Usage:**
 
 To run the script execute `python Kijiji-Scraper.py URL [-f] [-e] [-s]` the args are as follows:
 
 - `URL` the Kijiji URL to scrape for ads i.e. `https://www.kijiji.ca/b-calgary/kayak/k0l1700199?price=__1000` Any filters you use on Kijiji are part of the URL so they will apply to the script.
 
 - `-f` filename to store ads in i.e. `-f ads.txt` will store the ad ids in 'ads.txt'. The default filename is the URL.
 
 - `-e` words to exclude ads, can be one word or many seperated by spaces. `-e wanted used` will exclude any ads with the word wanted or used in the title.
 
 - `-s` flag to skip sending an email but will save the ad ids. This is useful for the first time you scrape a Kijiji URL as all the current ads will be indexed and after removing the flag you will only be sent new ads.
 
 The script can also be run with the `-h` arg to print out a help message i.e. `Kijiji-Scraper.py -h`
 
 **Example usage:**
 
 `python Kijiji-Scraper.py https://www.kijiji.ca/b-calgary/kayak/k0l1700199?price=__1000 -f kayaks.txt -e wanted` will find all ads for kayaks with a price of $1000 or less in Calgary and exclue any ads with 'wanted' in the title. The ads will be saved to kayaks.txt

`python Kijiji-Scraper.py https://www.kijiji.ca/b-calgary/kayak/k0l1700199?price=500__1000 -s` will find all kayak ads in calgary between $500 and $1000 and save them to a file with the url as the name. An email will not be sent in this case because of the -s flag.

**Dependencies: requests and BeautifulSoup**

`pip install requests`

`pip install bs4`

**How to run the script on set intervals:**

Windows:

The windows `Task Scheduler` can be used to have the script run at set intervals.

1. Create a new task
   - Fill in name and description

2. Add a trigger
   - Under `Settings` select `Daily`
   - Set `Repeat task every:` to your desired interval i.e. 5 mins to run the script every 5 mins
   - Set `for a duration of:` to indefinitely
   
3. Add an action
   - Action is Start a program
   - Set Program/script to the location of your python executable i.e. `C:\Users\{username}\AppData\Local\Programs\Python\Python36-32\pythonw.exe` (use pythonw.exe to run quietly, no window)
   - Set Add arguments to `Kijiji-Scraper.py URL` with any args wanted i.e. `Kijiji-Scraper.py https://www.kijiji.ca/b-calgary/kayak/k0l1700199?price=__1000 -f kayaks.txt -e wanted`
   - Set Start in to the location of the Kijiji-Scraper.py file i.e. `C:\Users\{username}\Documents\Scripts\`
   
4. Under Settings
   - Enable `Run task as soon as possible after a scheduled start is missed`
   
   
Linux:

Crontab can be used on linux to easily run the script on a set interval.
