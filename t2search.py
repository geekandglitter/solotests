# Explanation of delays:
# Implicit waits are used to provide a default waiting time between each consecutive test step/command across the entire test script. 
# Thus, the subsequent test step would only execute when the specified amount of time has elapsed after executing the previous test step/command.
# Explicit waits are used to halt the execution until the time a particular condition is met or the maximum time has elapsed. 
# Unlike Implicit waits, Explicit waits are applied for a particular instance only.
# Implicit Waits are not recommended

# System and Module Imports
import logging 
import sys
from datetime import datetime
import time
import requests
# Selenium Imports
from selenium import webdriver # The webdriver class connects to the browser's instance
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys  # The Keys class lets you emulate the stroke of keyboard keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
# browser Imports
from selenium.webdriver.firefox.options import Options
try:
    from msedge.selenium_tools import Edge, EdgeOptions
except:
    pass 
from selenium.webdriver.chrome import service
# browser Imports for Selenium 4
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service # couldn't get Service to work for Edge
from selenium.webdriver.safari.service import Service # untested of course
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Determine which platform
import os
import platform
 

class Search():    
    test_name = "Search 3" #class attribute      
    import selenium
    selenium_ver = selenium.__version__[0]   # Find out if we are running Selenium 4 or 3 (they have different API's)
    print("Selenium version is", selenium_ver)

    def __init__(self, initial_url, results_url, browse, keyword, running_platform):
        self.keyword = keyword
        self.initial_url = initial_url
        self.results_url = results_url
        self.browse=browse
        self.running_platform=running_platform
        if self.browse == "Chrome":  
            self.handler = self.setUpchrome()   # get the handler
        elif browse == "Firefox":
            self.handler = self.setUpfirefox()  # get the handler 
        elif browse == "Edge":
            self.handler = self.setUpedge()     # get the handler
        elif browse == "IE":
            self.handler = self.setUpIE()       # get the handler
        elif browse == "Safari":
            self.handler = self.setUpsafari()   # get the handler          
      

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return f"Initial URL is {self.initial_url}\nLanding URL is {self.results_url}"
 
     

    def setUpchrome(self):
        """Product name: unavailable Product version: unavailable 
        Running Chrome headless with sendkeys requires a window size"""
        options = webdriver.ChromeOptions()           
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless") 
        logging.info(f"{datetime.now(tz=None)} Info Looking for Chrome browser handler")  

        try:   
            if self.running_platform == "Darwin": # If it's a mac, then use the old API code regardless of Selenium version
                handler = webdriver.Chrome(options=options, executable_path='selenium_deps/drivers/chromedriver')   
            elif self.running_platform == "Windows" and Search.selenium_ver == "4": # If it's Windows, then check selenium version
                service = Service('selenium_deps\\drivers\\chromedriver.exe') # Specify the custom path (new for Selenium 4)            
                handler = webdriver.Chrome(options=options, service=service)  
            else: 
                handler = webdriver.Chrome(options=options,executable_path='selenium_deps\\drivers\\chromedriver.exe')        
            logging.info(f"{datetime.now(tz=None)} Info Chrome browser handler found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Chrome browser handler not found or failed to launch.")    
            handler = None  
        return handler         

    def setUpfirefox(self):
        """Product name: Firefox Nightly Product version: 71.0a1 
        Firefox can run headless with sendkeys. (Firefox handler is called GeckoDriver)"""  
        options = Options()
        options.headless = True
        logging.info(f"{datetime.now(tz=None)} Info Looking for Firefox browser handler") 
        
        try:
            if self.running_platform=="Darwin": # If it's a mac, then use the old API code regardless of Selenium version
                handler = webdriver.Firefox(options=options,executable_path='selenium_deps/drivers/geckodriver')  
            elif self.running_platform == "Windows" and Search.selenium_ver == "4": # If it's Windows, then check selenium version
                service = Service('selenium_deps\\drivers\\geckodriver.exe') # Specify the custom path (new for Selenium 4)
                handler = webdriver.Firefox(options=options, service=service)
            else:     
                handler = webdriver.Firefox(options=options,executable_path='selenium_deps\\drivers\\geckodriver.exe')  
            logging.info(f"{datetime.now(tz=None)} Info Firefox browser handler found")             
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Firefox browser handler not found or failed to launch.")    
            handler = None    
        return handler      

    def setUpedge(self):
        """Product name: Microsoft WebDriver Product version 83.0.478.58 
        * Edge gets wordy when it's headless, but at least it's working (by setting window size)
        * At the time of this refactor for Selenium 4, Edge does not yet support the new API, so I'm using the legacy one"""  
        options = EdgeOptions()
        options.use_chromium = True          
        #EdgeOptions.AddArguments("headless")  # this version of selenium doesn't have addarguments for edge
        options.headless = True # I got this to work by setting the handler window size  
        logging.info(f"{datetime.now(tz=None)} Info Looking for Edge browser handler")  
        try:        
            handler = Edge(executable_path='selenium_deps\\drivers\\msedgedriver.exe', options = options)   
            handler.set_window_size(1600, 1200)  # set the browser handler window size so that headless will work with sendkeys   
            logging.info(f"{datetime.now(tz=None)} Info Edge browser handler found")     
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Edge browser handler not found or failed to launch.")    
            handler = None                       
        return handler # ignore the handshake errors 
 


    def setUpsafari(self): # this Selenium (3) legacy API code works with both selenium 3 and selenium 4
        logging.info(f"{datetime.now(tz=None)} Info Looking for Safari browser handler")  
        try:
            handler = webdriver.Safari (executable_path='/usr/bin/safaridriver')
            handler.maximize_window() # necessary for sendkeys to work           
            logging.info
            (f"{datetime.now(tz=None)} Info Safari browser handler found")
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Safari browser handler not found or failed to launch.")    
            handler = None      
        return handler 


    def setUpIE(self):
        """Product name: Selenium WebDriver Product version: 2.42.0.0        
        IE does not have support for a headless mode
        IE has some other gotchas, too, which I posted in my blog. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """    
        logging.info(f"{datetime.now(tz=None)} Info Looking for IE browser handler")   
        try:  
            if Search.selenium_ver == "4":

                service = Service('selenium_deps\\drivers\\IEDriverServer.exe') # Specify the custom path (new for Selenium 4)  
                handler = webdriver.Ie(service=service)     
            else:
                handler = webdriver.Ie(executable_path = 'selenium_deps\\drivers\\IEDriverServer.exe')                 
            handler.implicitly_wait(2)
            handler.maximize_window()
            logging.info(f"{datetime.now(tz=None)} Info IE browser handler found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail IE browser handler not found or failed to launch.")    
            handler = None      
        return handler    

   
    def start_the_session(self): # This is where we load the website into the browser
        """See if the website is up and then get the session"""
        try:   
            resp = requests.get(self.initial_url)  # First make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} Info Looking for URL {self.initial_url}")
            if resp.status_code == 200:                
                self.handler.get(self.initial_url) # Now load the website
                # The .get() method waits for the page to render completely before moving on to the next step
                # time.sleep(10)   # ...so I took this sleep delay out
                print("The page title is", self.handler.title)
                logging.info(f"{datetime.now(tz=None)} Info URL {self.initial_url} found") 
                logging.info(f"{datetime.now(tz=None)} Info Session Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} Fail URL {self.initial_url} not found. Process terminated")    
            self.handler.quit()
            sys.exit(1)  
        import selenium
         

    def simulate_keyword_entry(self):
        """Find the search box and type in a single keyword which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info Looking for search box")
        try:   
            elem = WebDriverWait(self.handler, 10).until(            
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/label/input')) # We are looking inside the home session
            )        
            logging.info(f"{datetime.now(tz=None)} Info Search box found")
        except:
            logging.info(f"{datetime.now(tz=None)} Fail Search box not found")    
            self.handler.quit()
            sys.exit(1)
        elem.send_keys(self.keyword)  
        elem.send_keys(Keys.ENTER)  
        return

      
    def find_dropdown(self):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info Looking for search suggestion dropdown")  
        try:         
            elem=WebDriverWait(self.handler, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/div'))
            )    
            logging.info(f"{datetime.now(tz=None)} Info Found search suggestion dropdown")   
        except:  
            logging.info(f"{datetime.now(tz=None)} Fail Search suggestion dropdown not found")    
            self.handler.quit()
            sys.exit(1)     
        return    

    def find_search_suggestions(self):
        """Finding one search suggestion is enough evidence that the dropdown is correct"""    
        logging.info(f"{datetime.now(tz=None)} Info Looking for search suggestions") 
        try:            
            elem=WebDriverWait(self.handler, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/div/ul'))
            )    
            logging.info(f"{datetime.now(tz=None)} Info Found search suggestions")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} Fail Search suggestions not found")    
            self.handler.quit()
            sys.exit(1)  
        return    

    def verify_results_url(self):    # might need a webdriverwait until in here because of firefox   
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(4) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#                       
        if self.handler.current_url == self.results_url:              
            logging.info(f"{datetime.now(tz=None)} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} Fail with {self.handler.current_url} not equal to the expected ur: {self.results_url}")           
        return    

    def tearDown(self):    
        self.handler.quit()
        return

def main():
    """Selenium VERSION 4.0.0 Alpha 5 -- In Version 4 of Selenium, PhantomJS and Opera are no longer supported.
    Task: Create a Selenium test to simulate a search on a website and test that a results session is shown. Simulate entering a keyword for the keyword 's' without pressing enter. Results should be a list of suggestions
    About this script: https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
    """

    logging.basicConfig(filename='t2search.log', level=logging.INFO)        
    initial_url = "https://solosegment.com/" 
    results_url = f"{initial_url}?s=s" #class attribute
    keyword = "s"     
    running_platform = platform.system()    
    if running_platform =="Windows":
        browser_set = ["Chrome", "Firefox", "Edge","IE"]            
    elif running_platform =="Darwin": # Darwin is a mac
        browser_set=["Safari", "Chrome"] # still haven't gotten geckodriver (firefox) to work         
    elif running_platform =="Linux":   
        logging.info(f"{datetime.now(tz=None)} {running_platform} not yet supported")  
        sys.exit(1)     
    print("Running platform is", running_platform)
    for browse in browser_set:                   
        mysearch = Search(initial_url, results_url, browse, keyword, running_platform)              
        if mysearch.handler == None: # In the event that the handler is not found or failed to launch,
            continue # go on to the next browser rd   
        mysearch.start_the_session()          # start the session we want to test
        mysearch.simulate_keyword_entry()    
        mysearch.find_dropdown()
        mysearch.find_search_suggestions()
        mysearch.verify_results_url()     
        mysearch.tearDown()  
if __name__ == "__main__":
    main()