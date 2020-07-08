"""
 
NOTES:
1. This really should be written entirely in OOP, possibly with unittest as a testing framework 
2. From Stackoverflow: HTMLTestRunner module combined with unittest provides basic but robust HTML reports.
3. See https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click
 
## may or may not need these ### 
from   selenium.webdriver.support.ui import Select
from   selenium.common.exceptions import NoAlertPresentException 
import json
from selenium.webdriver.support import expected_conditions as EC
driver.current_url
driver.title
# The following might be useful for verifying the driver instance:
driver.name
driver.orientation
driver.page_source
driver.window_handles
driver.current_window_handle
driver.desired_capabilities
################
 Create a Selenium test to simulate a search on a website and test that a results page is shown. We can start with the
 SoloSegment.com site search as the first site to test with, but we will eventually create a test that can be used 
 any of our client's sites.
 Simulate entering a keyword for the letter 's' without pressing enter
 Results should be a list of suggestions
 """ 
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

"""
def __selenium_local_driver(self):
        browser_mapping = {
            'chrome': webdriver.Chrome,
            'firefox': webdriver.Firefox,
            'internet explorer': webdriver.Ie,
            'safari': webdriver.Safari,
            'edge': webdriver.Edge,
        }
"""

class Search():

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return self.url 

    def setUpchrome(self, url):
        """ Running Chrome headed so it will work with sendkeys"""
        options = webdriver.ChromeOptions()
        # options.add_argument("headless") # This is the correct syntax for headless                 
        logging.info(f"{datetime.now(tz=None)} Search Chrome Info Looking for chromedriver")  
        try:            
            self.driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)   
            logging.info(f"{datetime.now(tz=None)} Search Chrome Info Chromedriver found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Chrome Fail Chromedriver not found. Process terminated")    
            sys.exit(1)   
        return self.driver         

    def setUpfirefox(self,url):
        """Firefox can run headless with sendkeys. (Firefox driver is called GeckoDriver)"""  
        options = Options()
        options.headless = True
        logging.info(f"{datetime.now(tz=None)} Search Firefox Info Looking for geckodriver")  
        try:
            logging.info(f"{datetime.now(tz=None)} Search Firefox Info Geckodriver found") 
            self.driver = webdriver.Firefox(executable_path='c:\\data\\geckodriver\\geckodriver.exe', options=options)
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Firefox Fail Geckodriver not found. Process terminated")    
            sys.exit(1)     
        return self.driver         

    def setUpedge(self,url):
        """Setup for MS Edge. Sendkeys does not seem to work with headless Edge"""  
        options = EdgeOptions()
        options.use_chromium = True        
        #options.headless = True #This is the correct syntax for headless but we can't use it for sendkeys     
        logging.info(f"{datetime.now(tz=None)} Search Edge Info Looking for msedgedriver")  
        try:
            logging.info(f"{datetime.now(tz=None)} Search Edge Info msedgedriver found") 
            self.driver = Edge(executable_path='c:\\data\\msedgedriver\\msedgedriver.exe', options = options)            
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Edge Fail msedgedriver not found. Process terminated")    
            sys.exit(1)                     
        return self.driver # ignore the handshake errors  
   
    def navigate_to_page(self, driver, url, browse):
        try:   
            resp = requests.get(url)  # This is how we have to make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for URL {url}")
            if resp.status_code == 200:                
                driver.get(self.url)
                logging.info(f"{datetime.now(tz=None)} Search {browse} Info URL {url} found") 
                logging.info(f"{datetime.now(tz=None)} Search {browse} Info Headed Chrome Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail URL {url} not found. Process terminated")    
            driver.quit()
            sys.exit(1)                 
        return self.driver

    def simulate_single_letter_search(self, driver, letter, browse):
        """Find the search box and type in a single letter which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for search box")
        try:               
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Search box found")
        except (NoSuchElementException):
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail Search box not found")    
            driver.quit()
            sys.exit(1)
        elem.send_keys(letter)  
        elem.send_keys(Keys.ENTER)  
        return
 
    def find_dropdown(self,driver, browse):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for search suggestion dropdown")  
        try:         
            time.sleep(3)   
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div')
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Found search suggestion dropdown")   
        except (NoSuchElementException):  
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail Search suggestion dropdown not found")    
            driver.quit()
            sys.exit(1)     

    def find_a_suggestion(self,driver, browse):
        """ Now that we've found the dropdown, it seems reasonable there should be at least one suggestion in the list"""    
        logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for one search suggestion") 
        try:            
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div/ul')
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Found one search suggestion")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail Search suggestion not found")    
            driver.quit()
            sys.exit(1)  

    def verify_new_url(self, driver, new_url, browse):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(3) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#                       
        if driver.current_url == new_url:              
            logging.info(f"{datetime.now(tz=None)} Search {browse} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail with {driver.current_url}")           
        return driver  

    def tearDown(self, driver):         
        driver.close() 
        return  

def main():
    logging.basicConfig(filename='t2search.log', level=logging.INFO)   
    logging.warning("\n")
    url = "https://solosegment.com/" 
    # [Chrome, Firefox, Safari, Ie, Edge, PhantomJS]
 
    for browse in ["Chrome", "Firefox", "Edge"]:
    #for browse in ["Chrome", "Firefox", "Edge", "Safari", "Ie", "PhantomJS"]:    
  
        mysearch = Search(url)     
        if browse == "Chrome":  
            driver = mysearch.setUpchrome(url) 
        if browse == "Firefox":
            driver = mysearch.setUpfirefox(url)   
        if browse == "Edge":
            driver = mysearch.setUpedge(url)  


        driver= mysearch.navigate_to_page(driver, url, browse)         
        mysearch.simulate_single_letter_search(driver, 's', browse)    
        mysearch.find_dropdown(driver, browse)
        mysearch.find_a_suggestion(driver, browse) 
        new_url = f"{url}?s=s"
        driver = mysearch.verify_new_url(driver, new_url, browse)     
        mysearch.tearDown(driver)  

 

if __name__ == "__main__":
    main()
