# Questions for Mike:
#1. Do we need to run the test in other browsers?





# Documentation: https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webdriver 
# For info on webdriverwait https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
# More on webdriverwait until: https://selenium-python.readthedocs.io/waits.html#explicit-waits
import time
from selenium.webdriver.common.touch_actions import TouchActions 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  

def chrome_code(url):     
        
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    #options.add_argument("headless")  # When running headless, there are additional errors in the console, which don't seem to be a problem
    driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
    driver.get(url) 
    driver.implicitly_wait(60) # not sure which delay to use
    time.sleep(60)  # when this was set at 10 seconds, it wasn't enough time to load the page
    # Possible alternative to sleep is webdriverwait until but I don't yet see a reason to use it     
    return driver # ignore the handshake errors 
    #return driver.page_source

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

