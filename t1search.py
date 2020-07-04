"""
DISCUSS WITH MIKE:
1. This really should be written entirely in OOP, possibly with unittest as a testing framework 
2. From Stackoverflow: HTMLTestRunner module combined with unittest provides basic but robust HTML reports.
3. I haven't scratched the surface in how to log the results, but whatever I do will be too manual 
https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click
TODO:    
1. Logging format: search 1 pass/fail the fail message. All the tests go into one log file
2. Continue with Colt's Modern Python 3 Bootcamp  
3. Modularize the second check and refactor it to look in page source
4. Add firefox code
5. Fix the open file code to be OPEN WITH

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
from datetime import datetime

def chrome_setup(url): 
    """Chromedriver does not currently work with sendkeys in headless mode. See
    https://bugs.chromium.org/p/chromedriver/issues/detail?id=2521 
    """      
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")   
    driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    driver.get(url)          
    return driver # ignore the handshake errors   

def simulate_search_enter(driver, keyword):      
    """Simulate search by clicking enter""" 
    try:
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        print("Something went wrong. Search box not found. "  )   
        driver.quit()
        sys.exit(1)
    elem.send_keys(keyword)  
    elem.send_keys(Keys.ENTER)  
    return

def simulate_search_icon(driver, keyword):       
    """Simulate search by clicking the search icon"""
    try:
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        print("Something went wrong. Search box not found. "  )   
        driver.quit()
        sys.exit(1)

    elem.send_keys(keyword) 
    elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/input')
    webdriver.ActionChains(driver).move_to_element(elem).perform()  # perform moves the mouse now
    #time.sleep(20)
    elem.click()          
    return    

def verify_url(driver,keyword):       
    """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""       
    msg = "Pass\n"
    if driver.current_url != f"https://solosegment.com/?s={keyword}":    
        msg = f"Fail:\n{driver.current_url} is not the search results page\n"
    return msg    
#def verify_title(driver,keyword):
    """As an extra check, verify that the title "Search Results" is on the page"""      
    #assert "Search Results" in driver.page_source    # just added this as an alternative to the if below it
    #if  "Search Results" in driver.page_source:
        #msg_elem = f"Found the search title: 'Search Results'"             
    #else: 
        #msg_elem = f"Did not find search title: 'Search Results'"      
    #return msg_elem

def tear_down(driver): 
    time.sleep(20) # this just keeps the head up for 20 seconds
    driver.set_page_load_timeout(20) # This helps prevent Error reading broker pipe 
    driver.quit() # do not use driver.close()    
    return

def send_results(msg):
    f= open("t1log.txt","a+")
    f.write(f"{datetime.now(tz=None)}\n")
    f.write("Search 1\n")
    f.write(msg)          
    f.close()

def firefox_setup():
    """Consider using firefox for sendkeys with headless. (Firefox driver is called GeckoDriver)"""  

def main():
    url = "https://solosegment.com/"      
    driver = chrome_setup(url)    
    keyword = "solo_search"
    simulate_search_enter(driver, keyword)  
    #simulate_search_icon(driver, keyword)   
    msg = verify_url(driver, keyword) 
    #msg_elem = verify_title(driver, keyword)      
    tear_down(driver)
    send_results(msg)
     

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

