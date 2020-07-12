
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
# Browser Imports
from selenium.webdriver.firefox.options import Options
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome import service
# Browser Imports for Selenium 4
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service # couldn't get Service to work for Edge
from selenium.webdriver.safari.service import Service # untested of course
from selenium.webdriver.ie.service import Service

 

class Search():

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return self.url 

    def setUpchrome(self, test_name, browser):
        """Product name: unavailable Product version: unavailable 
        Running Chrome headless with sendkeys requires a window size"""
        options = webdriver.ChromeOptions()           
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless") 
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info Looking for driver")  

        try:
            service = Service('c:\\data\\chromedriver\\chromedriver.exe') # Specify the custom path (new for Selenium 4)            
            self.driver = webdriver.Chrome(options=options, service=service)   
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info  driver found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)   
        return self.driver         

    def setUpfirefox(self, test_name, browser):
        """Product name: Firefox Nightly Product version: 71.0a1 
        Firefox can run headless with sendkeys. (Firefox driver is called GeckoDriver)"""  
        options = Options()
        options.headless = True
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info Looking for driver") 
        
        try:
            service = Service('c:\\data\\geckodriver\\geckodriver.exe') # Specify the custom path (new for Selenium 4)
            self.driver = webdriver.Firefox(options=options, service=service)
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info driver found")             
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return self.driver         

    def setUpedge(self, test_name, browser):
        """Product name: Microsoft WebDriver Product version 83.0.478.58 
        * Edge gets wordy when it's headless, but at least it's working (by setting window size)
        * At the time of this refactor for Selenium 4, Edge does not yet support the new API, so I'm using the legacy one"""  
        options = EdgeOptions()
        options.use_chromium = True          
        #EdgeOptions.AddArguments("headless")  # this version of selenium doesn't have addarguments for edge
        options.headless = True # I got this to work by setting the driver window size  
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info Looking for driver")  
        try:
            self.driver = Edge(executable_path='c:\\data\\msedgedriver\\msedgedriver.exe', options = options)   
            self.driver.set_window_size(1600, 1200)  # set the driver window size so that headless will work with sendkeys   
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info driver found")     
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)                     
        return self.driver # ignore the handshake errors 


    def setUpsafari(self, test_name, browser):
        """I cannot currently test this safari code beause my only ios is on an old ipad Safari 12.4.7.  
        I posted a writeup on implementing Safari that might be of some help. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """ 
        return
        logging.info(f"{datetime.now(tz=None)} Search Safari Info Looking for driver")  
        try:       
            service = Service('/usr/bin/safaridriver') # Specify the custom path (new for Selenium 4)       
            self.driver = webdriver.Safari(options=options, service=service)    
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info driver found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return self.driver 

    def setUpIE(self, test_name, browser):
        """Product name: Selenium WebDriver Product version: 2.42.0.0
        IE does not have support for a headless mode
        IE has some other gotchas, too, which I posted in my blog. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """    
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info Looking for driver")   
        try:   
            service = Service('c:\\data\\iedriver\\IEDriverServer.exe') # Specify the custom path (new for Selenium 4)  
            self.driver = webdriver.Ie(service=service)                     
            self.driver.implicitly_wait(2)
            self.driver.maximize_window()
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info driver found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail driver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return self.driver 
    

   
    def get_the_page(self, driver, test_name, url, browse):
        """See if the page is up and then get the page"""
        try:   
            resp = requests.get(url)  # This is how we have to make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Looking for URL {url}")
            if resp.status_code == 200:                
                driver.get(self.url)
                time.sleep(10)   
                logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info URL {url} found") 
                logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Browser Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Fail URL {url} not found. Process terminated")    
            driver.quit()
            sys.exit(1)                 
        return self.driver

    def simulate_single_letter_search(self, driver, test_name, letter, browse):
        """Find the search box and type in a single letter which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Looking for search box")
        try:               
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Search box found")
        except (NoSuchElementException):
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Fail Search box not found")    
            driver.quit()
            sys.exit(1)
        elem.send_keys(letter)  
        elem.send_keys(Keys.ENTER)  
        return
 
    def find_dropdown(self,driver, test_name, browse):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Looking for search suggestion dropdown")  
        try:         
            time.sleep(3)   
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div')
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Found search suggestion dropdown")   
        except (NoSuchElementException):  
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Fail Search suggestion dropdown not found")    
            driver.quit()
            sys.exit(1)     

    def find_a_suggestion(self,driver, test_name, browse):
        """ Now that we've found the dropdown, it seems reasonable there should be at least one suggestion in the list"""    
        logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Looking for one search suggestion") 
        try:            
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div/ul')
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Info Found one search suggestion")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Fail Search suggestion not found")    
            driver.quit()
            sys.exit(1)  

    def verify_new_url(self, driver, test_name, new_url, browse):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(4) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#                       
        if driver.current_url == new_url:              
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} {test_name} {browse} Fail with {driver.current_url}")           
        return driver  

    def tearDown(self, driver):         
        #driver.close() 
        driver.quit()
        return  

def main():
    """Selenium VERSION 4.0.0 Alpha 5 -- In this version, PhantomJS and Opera are no longer supported
    Task: Create a Selenium test to simulate a search on a website and test that a results page is shown. We can start with the
    SoloSegment.com site search as the first site to test with, but we will eventually create a test that can be used with any of
    our client's sites. Simulate entering a keyword for the letter 's' without pressing enter. Results should be a list of suggestions
    About this script: https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
    """

    logging.basicConfig(filename='t2search.log', level=logging.INFO)   
    
    url = "https://solosegment.com/"  
    test_name = "Search 3"
    
    #for browse in  [ "Chrome", "Firefox", "Edge","IE", "Safari"]:  
    for browse in  [ "Chrome", "Firefox", "Edge","IE"]:        
      
        mysearch = Search(url)     
        print (mysearch)
        sys.exit(1) 
        if browse == "Chrome":  
            driver = mysearch.setUpchrome(test_name, browse)   # get the handler
        if browse == "Firefox":
            driver = mysearch.setUpfirefox(test_name, browse)  # get the handler 
        if browse == "Edge":
            driver = mysearch.setUpedge(test_name, browse)     # get the handler
        if browse == "IE":
            driver = mysearch.setUpIE(test_name, browse)       # get the handler
        if browse == "Safari":
            driver = mysearch.setUpsafari(test_name, browse)   # get the handler

        driver= mysearch.get_the_page(driver, test_name, url, browse)         # get the page we want to test
        mysearch.simulate_single_letter_search(driver, test_name, 's', browse)    
        mysearch.find_dropdown(driver, test_name, browse)
        mysearch.find_a_suggestion(driver, test_name, browse) 
        new_url = f"{url}?s=s"
        driver = mysearch.verify_new_url(driver, test_name, new_url, browse)     
        mysearch.tearDown(driver)  


if __name__ == "__main__":
    main()
