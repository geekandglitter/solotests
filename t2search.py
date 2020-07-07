
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

class Search():

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return self.url 

    def setUp(self):
        driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe")
        print("In setup", driver)
        driver.get(self.url)
        print("In setup", driver)
        return driver
         

    def verify_url(self, driver):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(3) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#    
        print(driver)
        if driver.current_url == "https://www.python.org":           
            logging.info(f"{datetime.now(tz=None)}  Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)}  Fail")           
        return driver  

    def tearDown(self, driver):
        print("in teardown", driver)
        driver.close() 
        return  


def main():
    logging.basicConfig(filename='t12earch.log', level=logging.INFO)   
    url = "https://www.python.org"  
    mysearch = Search(url)  
     
    driver = mysearch.setUp()
    print("In main", driver)
    driver = mysearch.verify_url(driver)
    print ("In main", driver)
    mysearch.tearDown(driver)
    print("done")
    


if __name__ == "__main__":
    main()
