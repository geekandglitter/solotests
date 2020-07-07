
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
from selenium import webdriver 
import logging 
import sys
from datetime import datetime
import time
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

class Search():

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return self.url 

    def setUpchrome(self, url):
        logging.info(f"{datetime.now(tz=None)} Search Chrome Info Looking for chromedriver")  
        try:            
            self.driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe")   
            logging.info(f"{datetime.now(tz=None)} Search Chrome Info Chromedriver found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Chrome Fail Chromedriver not found. Process terminated")    
            sys.exit(1)   
        try:   
            resp = requests.get(url)  
            if resp.status_code == 200:                
                self.driver.get(self.url)
            logging.info(f"{datetime.now(tz=None)} Search Chrome Info {url} found")      
        except:             
            logging.info(f"{datetime.now(tz=None)} Search Chrome Fail URL {url} not found. Process terminated")    
            self.driver.quit()
            sys.exit(1)                 
        return self.driver 

    def setUpfirefox(self,url):
        """Firefox can run headless with sendkeys. (Firefox driver is called GeckoDriver)"""  
        options = Options()
        options.headless = True
        logging.info(f"{datetime.now(tz=None)} Search Firefox Info Looking for geckodriver")  
        try:
            logging.info(f"{datetime.now(tz=None)} Search Firefox Info Geckodriver found") 
            driver = webdriver.Firefox(executable_path='c:\\data\\geckodriver\\geckodriver.exe', options=options)
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Firefox Fail Geckodriver not found. Process terminated")    
            sys.exit(1)     
        try:   
            resp = requests.get(url)  
            if resp.status_code == 200:
                driver.get(url) 
                logging.info(f"{datetime.now(tz=None)} Search Firefox Info URL {url} found") 
                logging.info(f"{datetime.now(tz=None)} Search Firefox Info Headless Firefox Initialized") 
        except:
            logging.info(f"{datetime.now(tz=None)} Search Firefox Fail URL {url} not found. Process terminated")    
            driver.quit()
            sys.exit(1)               
        return driver # ignore the handshake errors 


    def simulate_single_letter_search(self, driver, letter):
        """Find the search box and type in a single letter which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Search Chrome Info Looking for search box")
        try:               
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
            logging.info(f"{datetime.now(tz=None)} Search Chrome Info Search box found")
        except (NoSuchElementException):
            logging.info(f"{datetime.now(tz=None)} Search Chrome Fail Search box not found")    
            driver.quit()
            sys.exit(1)
        elem.send_keys(letter)  
        elem.send_keys(Keys.ENTER)  
        return
 
    def find_dropdown(self,driver):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} Search Chrome Info Looking for search suggestion dropdown")  
        try:         
            time.sleep(3)   
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div')
            logging.info(f"{datetime.now(tz=None)} Search Chrome Info Found search suggestion dropdown")   
        except (NoSuchElementException):  
            logging.info(f"{datetime.now(tz=None)} Search Chrome Fail Search suggestion dropdown not found")    
            driver.quit()
            sys.exit(1)     

    def find_a_suggestion(self,driver):
        """ Now that we've found the dropdown, it seems reasonable there should be at least one suggestion in the list"""    
        logging.info(f"{datetime.now(tz=None)} Search Chrome Info Looking for one search suggestion") 
        try:            
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div/ul')
            logging.info(f"{datetime.now(tz=None)} Search Chrome Info Found one search suggestion")   
             
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} Search Chrome Fail Search suggestion not found")    
            driver.quit()
            sys.exit(1)  


    def verify_new_url(self, driver, new_url):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(3) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#    
                   
        if driver.current_url == new_url:              
            logging.info(f"{datetime.now(tz=None)} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} Fail with {driver.current_url}")           
        return driver  

    def tearDown(self, driver):         
        driver.close() 
        return  

def main():
    logging.basicConfig(filename='t2search.log', level=logging.INFO)   
    logging.warning("\n")
    url = "https://solosegment.com/" 
    
    mysearch = Search(url)       
    driver = mysearch.setUpchrome(url)    
    mysearch.simulate_single_letter_search(driver, 's')    
    mysearch.find_dropdown(driver)
    mysearch.find_a_suggestion(driver) 
    new_url = f"{url}?s=s"
    driver = mysearch.verify_new_url(driver, new_url)     
    mysearch.tearDown(driver)   


    mysearch = Search(url)       
    driver = mysearch.setUpfirefox(url)    
    mysearch.simulate_single_letter_search(driver, 's')    
    mysearch.find_dropdown(driver)
    mysearch.find_a_suggestion(driver) 
    new_url = f"{url}?s=s"
    driver = mysearch.verify_new_url(driver, new_url)     
    mysearch.tearDown(driver)   


if __name__ == "__main__":
    main()
