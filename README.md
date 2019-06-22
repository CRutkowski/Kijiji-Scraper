# Kijiji-Scraper 3.0.0
### Python 3 program that scrapes Kijiji ad information and sends out an email when a new ads are found.


 **Config setup (config.yaml)**
 
 - Set the `sender`, `password` and `receiver` fields in the `config.yaml` file.
 
 - Specify the Kijji URLs you wish to scrape at the bottom of the config file. There are a few examples in the config to show the syntax.


Note: If you're using gmail, you'll have to go to 'My Account>Sign in & security>Connected apps & sites' then turn "Allow less secure apps" to "On" to allow the script to sign into gmail.


**Dependencies: requests, BeautifulSoup and PyYaml**

Run `pip3 install -r requirements.txt` to install all the dependencies

 
 **Usage:**
 
 To run the script execute `python3 main.py [-s]`
 
 - `-s` Optional flag to skip sending an email. This is useful for the first time you scrape a Kijiji as the current ads will be indexed and after removing the flag you will only be sent new ads.


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
