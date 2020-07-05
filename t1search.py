
"""
 
NOTES:
1. This really should be written entirely in OOP, possibly with unittest as a testing framework 
2. From Stackoverflow: HTMLTestRunner module combined with unittest provides basic but robust HTML reports.
3. I haven't scratched the surface in how to log the results, but whatever I do will be too manual 
https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click
4. Logging format: search 1 pass/fail the fail message. All the tests go into one log file

 
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
from selenium.common.exceptions import WebDriverException
import logging
import unittest
import sys
from datetime import datetime
from selenium.webdriver.firefox.options import Options
import requests

def chrome_setup(url, testnum): 
    """Chromedriver does not currently work with sendkeys in headless mode. See
    https://bugs.chromium.org/p/chromedriver/issues/detail?id=2521 
    """      
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")   
    try:
        driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    except (WebDriverException):
        logging.info(f"{datetime.now(tz=None)} Search {testnum} Chrome Fail Chromedriver not found. Process terminated")    
        #driver.quit()
        sys.exit(1) 
    try:        
        resp = requests.get(url)  
        if resp.status_code == 200:  
            driver.get(url)
            logging.info(f"{datetime.now(tz=None)} Search {testnum} Chrome Info URL {url} found")             
    except:
        logging.info(f"{datetime.now(tz=None)} Search {testnum} Chrome Fail URL {url} not found. Process terminated")    
        driver.quit()
        sys.exit(1)          
    return driver # ignore the handshake errors   

def firefox_setup(url, testnum):
    """Consider using firefox for sendkeys with headless. (Firefox driver is called GeckoDriver)"""  
    options = Options()
    options.headless = True
    try:
        driver = webdriver.Firefox(executable_path='c:\\data\\geckodriver\\geckodriver.exe', options=options)
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} Search {testnum} Firefox Fail Geckodriver not found. Process terminated")    
        #driver.quit()
        sys.exit(1)     
    try:
        resp = requests.get(url)  
        if resp.status_code == 200:
            driver.get(url) 
            logging.info(f"{datetime.now(tz=None)} Search {testnum} Firefox Info URL {url} found") 
            logging.info(f"{datetime.now(tz=None)} Search {testnum} Firefox Info Headless Firefox Initialized") 
    except:
        logging.info(f"{datetime.now(tz=None)} Search {tetnum} Firefox Fail URL {url} not found. Process terminated")    
        driver.quit()
        sys.exit(1)               
    return driver # ignore the handshake errors   

def simulate_search_enter(driver, keyword, testnum, browser):      
    """Simulate search by clicking enter""" 
    try:
        logging.info(f"{datetime.now(tz=None)} Search {testnum} {browser} Info Starting search box for ENTER simulation")   
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} Search {testnum} {browser} Fail Search box not found")    
        driver.quit()
        sys.exit(1)
    elem.send_keys(keyword)  
    elem.send_keys(Keys.ENTER)  
    return

def simulate_search_icon(driver, keyword, testnum, browser):       
    """Simulate search by clicking the search icon"""     
    try:
        logging.info(f"{datetime.now(tz=None)} Search {testnum} {browser} Info Starting search box for ICON simulation") 
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} Search {testnum} {browser} Fail Search box not found")       
        driver.quit()
        sys.exit(1)  

    elem.send_keys(keyword) 
    elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/input')
    webdriver.ActionChains(driver).move_to_element(elem).perform()  # perform moves the mouse now     
    elem.click()          
    return    

def verify_url(driver,keyword, testnum, browser):       
    """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
    time.sleep(3) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#    
    
    if driver.current_url == f"https://solosegment.com/?s={keyword}":           
        logging.info(f"{datetime.now(tz=None)} Search {testnum} {browser} Pass")  
    else: 
        logging.info(f"{datetime.now(tz=None)} Search {testnum} {browser} Fail {driver.current_url} is not the search results page")           
    return      

def tear_down(driver, testnum, browser):  
    """ Quit the driver """
    driver.set_page_load_timeout(20) # This helps prevent Error reading broker pipe 
    driver.quit() # do not use driver.close()   
    logging.info(f"{datetime.now(tz=None)} Search {testnum} {browser} Info Driver closed") 

    return        


def main():
    """This script runs two search box tests, each on two browsers"""
    url = "https://solosegment.com/"   
    #url = "https://sssssss.com/"   
    keyword = "solo_search"  
    logging.basicConfig(filename='searchtest.log', level=logging.INFO)     

 

    logging.info(f"{datetime.now(tz=None)} Search 1 Firefox Info Starting")
    driver = firefox_setup(url,1 )
    simulate_search_enter(driver, keyword, 1, "Firefox")  
    msg = verify_url(driver, keyword, 1, "Firefox")          
    tear_down(driver, 1, "Firefox")
     
    
    logging.info(f"{datetime.now(tz=None)} Search 2 Firefox Info Starting")
    driver = firefox_setup(url,2)
    simulate_search_icon(driver, keyword, 2, "Firefox")   
    msg = verify_url(driver, keyword, 2, "Firefox")          
    tear_down(driver, 2, "Firefox")
    

 

    logging.info(f"{datetime.now(tz=None)} Search 1 Chrome Info Starting")
    driver = chrome_setup(url,1)   
    simulate_search_enter(driver, keyword, 1, "Chrome") 
    msg = verify_url(driver, keyword, 1, "Chrome") 
    tear_down(driver, 1, "Chrome")
    

    logging.info(f"{datetime.now(tz=None)} Search 2 Chrome Info Starting")
    driver = chrome_setup(url,2)
    simulate_search_icon(driver, keyword, 2, "Chrome") 
    msg = verify_url(driver, keyword, 2, "Chrome")          
    tear_down(driver, 2, "Chrome")
     
     

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
 
