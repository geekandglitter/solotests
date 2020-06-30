# Questions for Mike:
#1. Do we need to run the test in other browsers?

# TODO:
"""
Fix the delay 
Read the Selenium materials I bookmarked
Continue with Colt's Modern Python 3 Bootcamp

"""


# Documentation: https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webdriver 
# For info on webdriverwait https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
# More on webdriverwait until: https://selenium-python.readthedocs.io/waits.html#explicit-waits
import time
from selenium.webdriver.common.touch_actions import TouchActions 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def chrome_code(url):     
        
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    #options.add_argument("headless")  # When running headless, there are additional errors in the console, which don't seem to be a problem
    driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    driver.get(url) 
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/label/input'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")
        driver.quit()      
    return driver # ignore the handshake errors 
    

def firefox_code():
    # uses GeckoDriver
    pass

def main():
    url = "https://solosegment.com/"
    driver = chrome_code(url)
    elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') 
    elem.send_keys("solosegment_monitoring_test")  
    elem.send_keys(Keys.ENTER)
    #elem.send_keys(Keys.
    time.sleep(60)

    search_url = driver.current_url
    if search_url == "https://solosegment.com/?s=solosegment_monitoring_test":
        print("Found Search Results Page:", search_url)
    

    # also look for this: <h1 class="page-title">Search Results for: <span>solosegment_monitoring_test</span></h1>

    driver.quit() # do not use driver.close()

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

