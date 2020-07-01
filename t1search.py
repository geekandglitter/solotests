"""
TODO:   
 
1. Logging format: search 1 pass/fail the fail message
2. Continue with Colt's Modern Python 3 Bootcamp 
3. Modularize the code in main
4. Suggestions for test reports from https://stackoverflow.com/questions/10218679/seleniumpython-reporting:
    To start building test reports on top of Selenium+Python, I would leverage the python unittest module.
    You will get a basic sample in Selenium documentation here.
    Then HTMLTestRunner module combined with unittest provides basic but robust HTML reports.

"""
 
 
## may or may not need these ### 
from   selenium.webdriver.support.ui import Select
from   selenium.common.exceptions import NoSuchElementException
from   selenium.common.exceptions import NoAlertPresentException 
import logging
import json
################


#### these are in use #####
import time
from selenium.webdriver.common.touch_actions import TouchActions 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





def chrome_setup(url): 
    """ Chromedriver does not currently work with sendkeys in headless mode. See
    https://bugs.chromium.org/p/chromedriver/issues/detail?id=2521
    Firefox reportedly does work for this.
    """
      
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")   
    driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    driver.get(url)          
    return driver # ignore the handshake errors     


def firefox_setup():
    # uses GeckoDriver
    pass

def main():
    url = "https://solosegment.com/"      
    driver = chrome_setup(url)   


    ### Turn this into send the search arg function     
    elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') 
    elem.send_keys("solosegment_monitoring_test")  
    elem.send_keys(Keys.ENTER) 


    # Now we should be in the search results page!     
    # Check to see if we are on the correct url which is https://solosegment.com/?s=solosegment_monitoring_test   
    # Turn this into verify url function  
    search_url = driver.current_url
    if search_url == "https://solosegment.com/?s=solosegment_monitoring_test":
        print("Found Search Results Page:", search_url)    
 

    # Now check on the page-title which should be "Search Results for: <span>solosegment_monitoring_test</span>"     
    #Looking for <h1 class="page-title">Search Results for: <span>solosegment_monitoring_test</span></h1>  
    # Turn this into Find the Title function 
    driver.implicitly_wait(10)
    element = driver.find_element(By.XPATH, '//*[@id="ss-search-title"]/h2')     
    if element.text == "Search Results":
        print(f"Found Search Title: '{element.text}'")    
    driver.set_page_load_timeout(20) # This helps prevent Error reading broker pipe 



    # Turn this into tearDown function
    time.sleep(20) # this just keeps the head up for 20 seconds
    driver.quit() # do not use driver.close()


    ### Turn this into send results to the log file
    pass

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

