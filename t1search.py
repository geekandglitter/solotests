"""
TODO:   
 
1. Logging format: search 1 pass/fail the fail message
2. Continue with Colt's Modern Python 3 Bootcamp 
3. Suggestions for test reports from https://stackoverflow.com/questions/10218679/seleniumpython-reporting:
    To start building test reports on top of Selenium+Python, I would leverage the python unittest module.
    You will get a basic sample in Selenium documentation here.
    Then HTMLTestRunner module combined with unittest provides basic but robust HTML reports.
4. Page objects and unittest https://selenium-python.readthedocs.io/page-objects.html    
5. Add exceptions such as NoSuchElementException

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

def simulate_search(driver):       
    try:
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        print("Something went wrong. Search box not found. ")     
        driver.quit()
        sys.exit(1)
    elem.send_keys("solosegment_monitoring_test")  
    elem.send_keys(Keys.ENTER)  
    return

def verify_results(driver):    
    # 1. Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test       
    if driver.current_url == "https://solosegment.com/?s=solosegment_monitoring_test":
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
    simulate_search(driver)     
    verify_results(driver)     
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

