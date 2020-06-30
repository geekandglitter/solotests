# Documentation: https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webdriver 
# For info on webdriverwait https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
# More on webdriverwait until: https://selenium-python.readthedocs.io/waits.html#explicit-waits
import time
from selenium.webdriver.common.touch_actions import TouchActions 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
  

def chrome_code(url):     
        
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("headless")  # When running headless, there are additional errors, which don't seem to be a problem
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
    url = "https://solosegment.com/?s=solosegment_monitoring_test"
    driver = chrome_code(url)
    if driver.current_url == url:
        print("Page URL is correct")
    driver.found_title =  driver.find_element_by_id('ss-search-title')   
    driver.found_search = driver.find_element_by_class_name('screen-reader-text')
    print("Search is", found_search)
    print("Type is", type(driver.found_title))
    print("Type of .text is", type(driver.found_title.text))   
    print("Found Title is", driver.found_title.text)
    print("Driver.current_url is", driver.current_url)
    print("The URL I put in was", url)    
    

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
'''