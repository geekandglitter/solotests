import time
from selenium.webdriver.common.touch_actions import TouchActions 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import logging 
import sys
from datetime import datetime
from selenium.webdriver.firefox.options import Options
import requests # Need this to make sure the URL is up and exists (driver.get() won't do that)

def firefox_setup(url, test_name, browser):
    """Consider using firefox for sendkeys with headless. (Firefox driver is called GeckoDriver)"""  
    options = Options()
    options.headless = True
    try:
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info driver found") 
        driver = webdriver.Firefox(executable_path='c:\\data\\geckodriver\\geckodriver.exe', options=options)
    except (WebDriverException):
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail driver not found. Process terminated")    
        sys.exit(1)     
    try:   
        resp = requests.get(url)  
        if resp.status_code == 200:
            driver.get(url) 
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info URL {url} found") 
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info {browser} Initialized") 
    except:
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail URL {url} not found. Process terminated")    
        driver.quit()
        sys.exit(1)               
    return driver # ignore the handshake errors 


def chrome_setup(url, test_name, browser): 
    """Chromedriver does not currently work with sendkeys in headless mode. See
    https://bugs.chromium.org/p/chromedriver/issues/detail?id=2521 
    """      
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")   
    try:
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info driver found") 
        driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    except (WebDriverException):
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail driver not found. Process terminated")    
        sys.exit(1) 
    try:        
        resp = requests.get(url)  
        if resp.status_code == 200:  
            driver.get(url)
            logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info URL {url} found")             
    except:
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail URL {url} not found. Process terminated")    
        driver.quit()
        sys.exit(1)          
    return driver # ignore the handshake errors         

def simulate_search_enter(driver, keyword, test_name, browser):      
    """Simulate search by clicking enter""" 
    try:
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info Starting search box for ENTER simulation")   
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail Search box not found")    
        driver.quit()
        sys.exit(1)
    elem.send_keys(keyword)  
    elem.send_keys(Keys.ENTER)  
    return

def simulate_search_icon(driver, keyword, test_name, browser):       
    """Simulate search by clicking the search icon"""     
    try:
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info Starting search box for ICON simulation") 
        elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
    except (NoSuchElementException):
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail Search box not found")       
        driver.quit()
        sys.exit(1)  
    elem.send_keys(keyword) 
    elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/input')
    webdriver.ActionChains(driver).move_to_element(elem).perform()  # perform moves the mouse now     
    elem.click()          
    return    

def verify_new_url(driver,keyword, test_name, browser):       
    """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
    time.sleep(3) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#    
    
    if driver.current_url == f"https://solosegment.com/?s={keyword}":           
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Pass")  
    else: 
        logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Fail {driver.current_url} is not the search results page")           
    return      

def tear_down(driver, test_name, browser):  
    """ Quit the driver """
    driver.set_page_load_timeout(20) # This helps prevent Error reading broker pipe 
    driver.quit() # do not use driver.close()   
    logging.info(f"{datetime.now(tz=None)} {test_name} {browser} Info Driver closed") 
    return        


def main():
    """This script runs two search box tests, each on two browsers"""
    url = "https://solosegment.com/"   
    
    keyword = "solo_search"  
    logging.basicConfig(filename='t1search.log', level=logging.INFO)   


    logging.info(f"{datetime.now(tz=None)} Search 1 Firefox Info Starting")
    driver = firefox_setup(url, "Search 1", "Firefox" )
    simulate_search_enter(driver, keyword, "Search1" , "Firefox")  
    msg = verify_new_url(driver, keyword, "Search 1", "Firefox")          
    tear_down(driver, "Search 1", "Firefox")     
    
    logging.info(f"{datetime.now(tz=None)} Search 2 Firefox Info Starting")
    driver = firefox_setup(url, "Search 2", "Firefox")
    simulate_search_icon(driver, keyword, "Search 2", "Firefox")   
    msg = verify_new_url(driver, keyword, "Search 2", "Firefox")          
    tear_down(driver, "Search 2", "Firefox") 

    logging.info(f"{datetime.now(tz=None)} Search 1 Chrome Info Starting")
    driver = chrome_setup(url, "Search 1", "Chrome")   
    simulate_search_enter(driver, keyword, "Search 1", "Chrome") 
    msg = verify_new_url(driver, keyword, "Search 1", "Chrome") 
    tear_down(driver, "Search 1", "Chrome")    

    logging.info(f"{datetime.now(tz=None)} Search 2 Chrome Info Starting")
    driver = chrome_setup(url,"Search 2", "Chrome")
    simulate_search_icon(driver, keyword, "Search 2", "Chrome") 
    msg = verify_new_url(driver, keyword, "Search 2", "Chrome")          
    tear_down(driver, "Search 2", "Chrome")     

if __name__=="__main__":
    main()

 
 
 
