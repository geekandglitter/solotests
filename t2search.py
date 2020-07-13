
# System and Module Imports
import logging 
import sys
from datetime import datetime
import time
import requests
# Selenium Imports
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
# browser Imports
from selenium.webdriver.firefox.options import Options
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome import service
# browser Imports for Selenium 4
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service # couldn't get Service to work for Edge
from selenium.webdriver.safari.service import Service # untested of course
from selenium.webdriver.ie.service import Service

 

class Search():    
    test_name = "Search 3" #class attribute       

    def __init__(self, initial_url, landing_url):
        self.initial_url = initial_url
        self.landing_url = landing_url

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return f"Initial URL is {self.initial_url}\nLanding URL is {self.landing_url}"


    def get_the_handler(self, browse, mysearch):
        if browse == "Chrome":  
            driver = mysearch.setUpchrome(browse, mysearch)   # get the handler
        elif browse == "Firefox":
            driver = mysearch.setUpfirefox (browse, mysearch)  # get the handler 
        elif browse == "Edge":
            driver = mysearch.setUpedge(browse, mysearch)     # get the handler
        elif browse == "IE":
            driver = mysearch.setUpIE(browse, mysearch)       # get the handler
        elif browse == "Safari":
            driver = mysearch.setUpsafari(browse, mysearch)   # get the handler
        return(driver)    
    

    def setUpchrome(self, browse, mysearch):
        """Product name: unavailable Product version: unavailable 
        Running Chrome headless with sendkeys requires a window size"""
        options = webdriver.ChromeOptions()           
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless") 
        logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for driver")  

        try:
            service = Service('c:\\data\\chromedriver\\chromedriver.exe') # Specify the custom path (new for Selenium 4)            
            driver = webdriver.Chrome(options=options, service=service)   
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info  driver found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)   
        return driver         

    def setUpfirefox(self, browse, mysearch):
        """Product name: Firefox Nightly Product version: 71.0a1 
        Firefox can run headless with sendkeys. (Firefox driver is called GeckoDriver)"""  
        options = Options()
        options.headless = True
        logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for driver") 
        
        try:
            service = Service('c:\\data\\geckodriver\\geckodriver.exe') # Specify the custom path (new for Selenium 4)
            driver = webdriver.Firefox(options=options, service=service)
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info driver found")             
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return driver         

    def setUpedge(self, browse, mysearch):
        """Product name: Microsoft WebDriver Product version 83.0.478.58 
        * Edge gets wordy when it's headless, but at least it's working (by setting window size)
        * At the time of this refactor for Selenium 4, Edge does not yet support the new API, so I'm using the legacy one"""  
        options = EdgeOptions()
        options.use_chromium = True          
        #EdgeOptions.AddArguments("headless")  # this version of selenium doesn't have addarguments for edge
        options.headless = True # I got this to work by setting the driver window size  
        logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for driver")  
        try:
            driver = Edge(executable_path='c:\\data\\msedgedriver\\msedgedriver.exe', options = options)   
            driver.set_window_size(1600, 1200)  # set the driver window size so that headless will work with sendkeys   
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info driver found")     
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)                     
        return driver # ignore the handshake errors 


    def setUpsafari(self, browse, mysearch):
        """I cannot currently test this safari code beause my only ios is on an old ipad Safari 12.4.7.  
        I posted a writeup on implementing Safari that might be of some help. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """ 
        return
        logging.info(f"{datetime.now(tz=None)} Search Safari Info Looking for driver")  
        try:       
            service = Service('/usr/bin/safaridriver') # Specify the custom path (new for Selenium 4)       
            driver = webdriver.Safari(options=options, service=service)    
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info driver found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return driver 

    def setUpIE(self, browse, mysearch):
        """Product name: Selenium WebDriver Product version: 2.42.0.0
        IE does not have support for a headless mode
        IE has some other gotchas, too, which I posted in my blog. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """    
        logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for driver")   
        try:   
            service = Service('c:\\data\\iedriver\\IEDriverServer.exe') # Specify the custom path (new for Selenium 4)  
            driver = webdriver.Ie(service=service)                     
            driver.implicitly_wait(2)
            driver.maximize_window()
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info driver found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return driver    

   
    def get_the_page(self, driver, browse):
        """See if the page is up and then get the page"""
        try:   
            resp = requests.get(self.initial_url)  # This is how we have to make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for URL {self.initial_url}")
            if resp.status_code == 200:                
                driver.get(self.initial_url)
                time.sleep(10)   
                logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info URL {self.initial_url} found") 
                logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info browse Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail URL {self.initial_url} not found. Process terminated")    
            driver.quit()
            sys.exit(1)                 
        return driver

    def simulate_single_letter_search(self, page, letter, browse):
        """Find the search box and type in a single letter which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for search box")
        try:               
            elem=page.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Search box found")
        except (NoSuchElementException):
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail Search box not found")    
            page.quit()
            sys.exit(1)
        elem.send_keys(letter)  
        elem.send_keys(Keys.ENTER)  
        return
 
    def find_dropdown(self, page, browse):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for search suggestion dropdown")  
        try:         
            time.sleep(3)   
            elem=page.find_element(By.XPATH, '//*[@id="search-6"]/form/div')
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Found search suggestion dropdown")   
        except (NoSuchElementException):  
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail Search suggestion dropdown not found")    
            page.quit()
            sys.exit(1)     
        return    

    def find_a_suggestion(self, page, browse):
        """ Now that we've found the dropdown, it seems reasonable there should be at least one suggestion in the list"""    
        logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Looking for one search suggestion") 
        try:            
            elem=page.find_element(By.XPATH, '//*[@id="search-6"]/form/div/ul')
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Info Found one search suggestion")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail Search suggestion not found")    
            page.quit()
            sys.exit(1)  
        return    

    def verify_landing_url(self, page, browse):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(4) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#                       
        if page.current_url == self.landing_url:              
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} {Search.test_name} {browse} Fail with {page.current_url} not equal to {self.landing_url}")           
        return page  

    def tearDown(self, page):    
        page.quit()
        return

def main():
    """Selenium VERSION 4.0.0 Alpha 5 -- In this version, PhantomJS and Opera are no longer supported
    Task: Create a Selenium test to simulate a search on a website and test that a results page is shown. We can start with the
    SoloSegment.com site search as the first site to test with, but we will eventually create a test that can be used with any of
    our client's sites. Simulate entering a keyword for the letter 's' without pressing enter. Results should be a list of suggestions
    About this script: https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
    """

    logging.basicConfig(filename='t2search.log', level=logging.INFO)      
    initial_url = "https://solosegment.com/" 
    landing_url = f"{initial_url}?s=s" #class attribute

    for browse in  [ "Chrome", "Firefox", "Edge","IE"]:      #for browse in  [ "Chrome", "Firefox", "Edge","IE", "Safari"]:      
        mysearch = Search(initial_url, landing_url)     
        driver = mysearch.get_the_handler(browse, mysearch)  # get the handler for the browser
        page= mysearch.get_the_page(driver, browse)          # get the page we want to test
        mysearch.simulate_single_letter_search(page, 's', browse)    
        mysearch.find_dropdown(page, browse)
        mysearch.find_a_suggestion(page, browse) 
        page = mysearch.verify_landing_url(page, browse)     
        mysearch.tearDown(page)  
if __name__ == "__main__":
    main()
