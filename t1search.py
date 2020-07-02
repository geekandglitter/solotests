"""
DISCUSS WITH MIKE:
1. This really should be written entirely in OOP, possibly with unittest as a testing framework 
2. From Stackoverflow: HTMLTestRunner module combined with unittest provides basic but robust HTML reports.
3. I haven't scratched the surface in how to log the results, but whatever I do will be too manual

UPDATE FROM MIKE:

- The developers do prefer headless, but not if it means you can't test the ENTER key, so maybe keep it Chrome and headed for now.
- You can initiate a search by clicking the search icon in the search input box as well as by pressing enter, so that should be maybe 
created as an additional test.
- Running from the command line is OK, at least for now.
- Creating a log as we discussed is fine, too.
  

TODO:    
1. Logging format: search 1 pass/fail the fail message
2. Continue with Colt's Modern Python 3 Bootcamp 
3. Look into the free trial of Robot Framework or GhostInspector or Testcraft


## may or may not need these ### 
from   selenium.webdriver.support.ui import Select
from   selenium.common.exceptions import NoAlertPresentException 
import json
from selenium.webdriver.support import expected_conditions as EC
################
""" 
 
import time
from selenium.webdriver.common.touch_actions import TouchActions 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import logging
import unittest
import sys

def chrome_setup(url): 
    """Chromedriver does not currently work with sendkeys in headless mode. See
    https://bugs.chromium.org/p/chromedriver/issues/detail?id=2521 
    """      
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")   
    driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    driver.get(url)          
    return driver # ignore the handshake errors   

def simulate_search(driver, keyword):       
    try:
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        print("Something went wrong. Search box not found. ")     
        driver.quit()
        sys.exit(1)
    elem.send_keys(keyword)  
    elem.send_keys(Keys.ENTER)  
    return

def verify_results(driver, keyword):    
    # 1. Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test       
    if driver.current_url == f"https://solosegment.com/?s={keyword}":
        print("Found Search Results Page:", driver.current_url)  

    # 2. Check on the title 
    driver.implicitly_wait(10)
    try:
        expected_xpath = '//*[@id="ss-search-title"]/h2'
        elem = driver.find_element(By.XPATH, expected_xpath )  # We are looking inside the search results page 
    except (NoSuchElementException):
        print(f"Did not find the expected XPATH {expected_xpath} on the page.")  
        driver.quit()
        sys.exit(1)
    if elem.text == "Search Results":
        print(f"Found Search Title: '{elem.text}'")       
    return

def tear_down(driver): 
    time.sleep(20) # this just keeps the head up for 20 seconds
    driver.set_page_load_timeout(20) # This helps prevent Error reading broker pipe 
    driver.quit() # do not use driver.close()    
    return

def send_results():
    pass        

def firefox_setup():
    """Consider using firefox for sendkeys with headless. (Firefox driver is called GeckoDriver)"""  

def main():
    url = "https://solosegment.com/"      
    driver = chrome_setup(url)    
    keyword = "solo_search"
    simulate_search(driver, keyword)     
    verify_results(driver, keyword)     
    tear_down(driver)
    send_results()
     

if __name__=="__main__":
    main()

 

 



'''
driver.current_url
driver.title

# The following might be useful for verifying the driver instance:
driver.name
driver.orientation
driver.page_source
driver.window_handles
driver.current_window_handle
driver.desired_capabilities
 

//*[@id="search-6"]/form/label/input
//*[@id="search-6"]/form/label/input

// FULL XPATH
/html/body/div[1]/header/div[1]/div/div/div/div[2]/div/form/label/input
'''

