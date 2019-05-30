# Kijiji-Scraper 2.6
### Python 3 script that scrapes Kijiji ad information and sends out an email when a new ad is found.


 **Config setup**
 
 - Set the `sender`, `passwd` and `receiver` fields in the config.py file.
 
 - The `urls_to_scrape` field is a list of dictionary objects containing a Kijiji URL to scrape and an optional list of words to exclude. You will need to add a new dictionary object for each URL you want to scrape. There are two examples in the config.


Note: If you're using gmail, you'll have to go to 'My Account>Sign in & security>Connected apps & sites' then turn "Allow less secure apps" to "On" to allow the script to sign into gmail.


**Dependencies: requests and BeautifulSoup**

Run `pip install -r requirements.txt` to install all dependencies

 
 **Usage:**
 
 To run the script execute `python3 main.py [-s]`
 
 - `-s` flag to skip sending an email but will save the ad ids. This is useful for the first time you scrape a Kijiji URL as all the current ads will be indexed and after removing the flag you will only be sent new ads.


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
   - Set Add arguments to `main.py`
   - Set Start in to the location of the main.py file i.e. `C:\Users\{username}\Documents\Scripts\Kijiji-Scraper\`
   
4. Under Settings
   - Enable `Run task as soon as possible after a scheduled start is missed`
   
   
Linux:

Crontab can be used on linux to easily run the script on a set interval.
