
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
import logging
import unittest
import sys
from datetime import datetime
from selenium.webdriver.firefox.options import Options

def chrome_setup(url): 
    """Chromedriver does not currently work with sendkeys in headless mode. See
    https://bugs.chromium.org/p/chromedriver/issues/detail?id=2521 
    """      
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")   
    try:
        driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} Chromedriver not found. Process terminated.")    
        driver.quit()
        sys.exit(1) 
    try:
        driver.get(url)    
        logging.info(f"{datetime.now(tz=None)} URL {url} found.") 
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} URL {url} not found. Process terminated.")    
        driver.quit()
        sys.exit(1)          
    return driver # ignore the handshake errors   

def firefox_setup(url):
    """Consider using firefox for sendkeys with headless. (Firefox driver is called GeckoDriver)"""  
    options = Options()
    options.headless = True
    try:
        driver = webdriver.Firefox(executable_path='c:\\data\\geckodriver\\geckodriver.exe', options=options)
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} Geckodriver not found. Process terminated.")    
        driver.quit()
        sys.exit(1)     
    try:
        driver.get(url) 
        logging.info(f"{datetime.now(tz=None)} URL {url} found.") 
        logging.info(f"{datetime.now(tz=None)} Headless Firefox Initialized") 
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} URL {url} not found. Process terminated.")    
        driver.quit()
        sys.exit(1)               
    return driver # ignore the handshake errors   

def simulate_search_enter(driver, keyword):      
    """Simulate search by clicking enter""" 
    try:
        logging.info(f"{datetime.now(tz=None)} Starting search box for ENTER simulation")   
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} Search box not found")    
        driver.quit()
        sys.exit(1)
    elem.send_keys(keyword)  
    elem.send_keys(Keys.ENTER)  
    return

def simulate_search_icon(driver, keyword):       
    """Simulate search by clicking the search icon"""     

    try:
        logging.info(f"{datetime.now(tz=None)} Starting search box for ICON simulation") 
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} Search box not found")       
        driver.quit()
        sys.exit(1)  

    elem.send_keys(keyword) 
    elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/input')
    webdriver.ActionChains(driver).move_to_element(elem).perform()  # perform moves the mouse now     
    elem.click()          
    return    

def verify_url(driver,keyword):       
    """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
    time.sleep(1) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#    
    
    if driver.current_url == f"https://solosegment.com/?s={keyword}":           
        logging.info(f"{datetime.now(tz=None)} Pass")  
    else: 
        logging.info(f"{datetime.now(tz=None)} Fail: {driver.current_url} is not the search results page.")           
    return      

def tear_down(driver):  
    driver.set_page_load_timeout(20) # This helps prevent Error reading broker pipe 
    driver.quit() # do not use driver.close()   
    logging.info(f"{datetime.now(tz=None)} Driver closed") 
    return        


def main():
    url = "https://solosegment.com/"      
    keyword = "solo_search"  
    logging.basicConfig(filename='searchtest.log', level=logging.INFO) 
    logging.info('\n')

    logging.info(f"{datetime.now(tz=None)} Search 1 Firefox")
    driver = firefox_setup(url)
    simulate_search_enter(driver, keyword)  
    msg = verify_url(driver, keyword)          
    tear_down(driver)
    logging.info("\n")
    
    logging.info(f"{datetime.now(tz=None)} Search 2 Firefox")
    driver = firefox_setup(url)
    simulate_search_icon(driver, keyword)   
    msg = verify_url(driver, keyword)          
    tear_down(driver)
    logging.info("\n")

    logging.info(f"{datetime.now(tz=None)} Search 1 Chrome")
    driver = chrome_setup(url)   
    simulate_search_enter(driver, keyword) 
    msg = verify_url(driver, keyword) 
    tear_down(driver)
    logging.info("\n")

    logging.info(f"{datetime.now(tz=None)} Search 2 Chrome")
    driver = chrome_setup(url)
    simulate_search_icon(driver, keyword) 
    msg = verify_url(driver, keyword)          
    tear_down(driver)
    logging.info("\n")
    

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
 
