"""
DISCUSS WITH MIKE:
1. Selenium v4.0.0-alpha.1    https://www.selenium.dev/selenium/docs/api/javascript/page/Changes.html
For Opera, users should be able to simply rely on testing Chrome as the Opera browser is based on Chromium
(and the operadriver was a thin wrapper around chromedriver). 
For PhantomJS, users should use Chrome or Firefox in headless mode (see example/headless.js)
2. Can you ask your developers which browsers they think really must be tested? We have chrome, firefox, IE (headed only), Edge. Do we also need 
Opera(which is based on CHrome) and Edge Legacy?
3. RIght now I'm quitting out of the whole script if a driver isn't found. Maybe I should just move on to the next driver
4. Note: the driver I have doesn't even work in Opera 69.0.3686.57 but it does work in 69.0.3686.47, but Opera keeps updating itself. ALso I see 
that it doesn't work with the developer version: https://blogs.opera.com/desktop/2020/06/opera-71-developer/. Maybe they've dropped support
Plus note that Opera has no headless option, and is based on Chromium anyway. Not to mention I can't get rid of that flags error
5. I don't know but maybe the developers care that I'm not using the unittest module

NOTES to self:
1. I have a post with a link on how to use unittest
2. Also use that same post to refactor the browser set up some more
3. Find out what this is from Stackoverflow: HTMLTestRunner module combined with unittest provides basic but robust HTML reports.
4. And this: https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click
5. I Need to research capabilities options
 
## may or may not need these ### 
from   selenium.webdriver.support.ui import Select
from   selenium.common.exceptions import NoAlertPresentException 
import json
from selenium.webdriver.support import expected_conditions as EC
driver.current_url
driver.title

# The following might be useful for verifying the driver instance:
driver.name
driver.orientation
driver.page_source
driver.window_handles
driver.current_window_handle
driver.desired_capabilities
################
 
 """ 
# System and Module Imports
import logging 
import sys
from datetime import datetime
import time
import requests
# Selenium Imports
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
# Browser Imports
from selenium.webdriver.firefox.options import Options
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome import service
 

class Search():

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return self.url 

    def setUpchrome(self):
        """Product name: unavailable Product version: unavailable 
        Running Chrome headless with sendkeys required a window size"""
        options = webdriver.ChromeOptions()
           
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless")

        # options.add_argument("headless") # This is the correct syntax for headless                 
        logging.info(f"{datetime.now(tz=None)} Search Chrome Info Looking for chromedriver")  

        try:            
            self.driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)   
            logging.info(f"{datetime.now(tz=None)} Search Chrome Info Chromedriver found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Chrome Fail Chromedriver not found or driver failed to launch. Process terminated")    
            sys.exit(1)   
        return self.driver         

    def setUpfirefox(self):
        """Product name: Firefox Nightly Product version: 71.0a1 
        Firefox can run headless with sendkeys. (Firefox driver is called GeckoDriver)"""  
        options = Options()
        options.headless = True
        logging.info(f"{datetime.now(tz=None)} Search Firefox Info Looking for geckodriver")  
        try:
            self.driver = webdriver.Firefox(executable_path='c:\\data\\geckodriver\\geckodriver.exe', options=options)
            logging.info(f"{datetime.now(tz=None)} Search Firefox Info Geckodriver found")             
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Firefox Fail Geckodriver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return self.driver         

    def setUpedge(self):
        """Product name: Microsoft WebDriver Product version 83.0.478.58 
        Edge gets wordy when it's headless, but at least it's working (by setting window size)"""  
        options = EdgeOptions()
        options.use_chromium = True          
        #EdgeOptions.AddArguments("headless")  # this version of selenium doesn't have addarguments for edge
        options.headless = True # I got this to work by setting the driver window size  
        logging.info(f"{datetime.now(tz=None)} Search Edge Info Looking for msedgedriver")  
        try:
            self.driver = Edge(executable_path='c:\\data\\msedgedriver\\msedgedriver.exe', options = options)   
            self.driver.set_window_size(1600, 1200)  # set the driver window size so that headless will work with sendkeys   
            logging.info(f"{datetime.now(tz=None)} Search Edge Info msedgedriver found")     
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Edge Fail msedgedriver not found or driver failed to launch. Process terminated")    
            sys.exit(1)                     
        return self.driver # ignore the handshake errors 


    def setUpsafari(self):
        """I cannot currently test this safari code beause my only ios is on an old ipad Safari 12.4.7.  
        I posted a writeup on implementing Safari that might be of some help: https://speakingpython.blogspot.com/search/label/Safari
        """ 
        logging.info(f"{datetime.now(tz=None)} Search Safari Info Looking for safaridriver")  
        try:            
            self.driver = webdriver.Safari(executable_path = '/usr/bin/safaridriver')    
            logging.info(f"{datetime.now(tz=None)} Search Safari Info Safaridriver found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Safari Fail Safaridriver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return self.driver 

    def setUpIE(self):
        """Product name: Selenium WebDriver Product version: 2.42.0.0
        IE does not have support for a headless mode
        IE has some other gotchas, too, which I posted in my blog: https://speakingpython.blogspot.com/2020/07/selenium-webdriver-for-ie-gotchas.html
        """    
        logging.info(f"{datetime.now(tz=None)} Search IE Info Looking for IEDriverServer")   
        try:   
            self.driver = webdriver.Ie(executable_path='c:\\data\\iedriver\\IEDriverServer.exe')                     
            self.driver.implicitly_wait(2)
            self.driver.maximize_window()
            logging.info(f"{datetime.now(tz=None)} Search IE Info IEDriverServer found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search IE Fail IEDriverServer not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return self.driver 



    def setUpOpera(self):
        """Product name: unavailable Product version: unavailable 
        This is working but with an error in Opera which is this:
        You are using an unsupported command-line flag: --enable-blink-features=shadow DOM V0. stability and security will suffer.
        but then I updated Opera and now it doesn't work at all
        then I uninstalled it and reinstalled the 47 version for "all users"
        Now it works again but I'm still getting that flag message
        https://github.com/operasoftware/operachromiumdriver/blob/master/docs/desktop.md 
        headless is not supported in Opera
        There are 2 types of Opera - Java Based and Chrominium based.
        The provided links are for Java based Opera.
        https://github.com/operasoftware/operadriver#desktop
        There is no official support for latest Opera versions.
        OperaPrestoDriver is only compatible with Presto-based Opera browsers up until v12.1*. 
        For Blink-based Operas (v15 and onwards), refer to the OperaChromiumDriver project.
        I finally found enable-blink-features here: https://peter.sh/experiments/chromium-command-line-switches/
        Note: the driver I have doesn't even work in Opera 69.0.3686.57 but it does work in 69.0.3686.47, but Opera keeps updating itself. 
        Plus note that Opera has no headless option, and is based on Chromium anyway. Not to mention I can't get rid of that flags error

         
         
        """    
        logging.info(f"{datetime.now(tz=None)} Search Opera Info Looking for operadriver")   
        try:               
            options = webdriver.ChromeOptions()                
            #options.headless = True       
            #options.add_argument("window-size=1920x1080")
            #options.add_argument("headless")


            #options.binary_location = "C:\\Users\\Linda\\AppData\\Local\\Programs\\Opera\\launcher.exe"
            self.driver = webdriver.Opera(executable_path="c:\\data\\operadriver_win64\\operadriver.exe", options=options)
            #self.driver.set_window_size(1600, 1200)         
            self.driver.implicitly_wait(2)       
            #self.driver.maximize_window()
              # set the driver window size so that headless will work with sendkeys  
            logging.info(f"{datetime.now(tz=None)} Search Opera Info operadriver found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Search Opera Fail operadriver not found or driver failed to launch. Process terminated")    
            sys.exit(1)     
        return self.driver 

   
    def get_the_page(self, driver, url, browse):
        """See if the page is up and then get the page"""
        try:   
            resp = requests.get(url)  # This is how we have to make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for URL {url}")
            if resp.status_code == 200:                
                driver.get(self.url)
                time.sleep(10)
                logging.info(f"{datetime.now(tz=None)} Search {browse} Info URL {url} found") 
                logging.info(f"{datetime.now(tz=None)} Search {browse} Info Browser Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail URL {url} not found. Process terminated")    
            driver.quit()
            sys.exit(1)                 
        return self.driver

    def simulate_single_letter_search(self, driver, letter, browse):
        """Find the search box and type in a single letter which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for search box")
        try:               
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home page
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Search box found")
        except (NoSuchElementException):
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail Search box not found")    
            driver.quit()
            sys.exit(1)
        elem.send_keys(letter)  
        elem.send_keys(Keys.ENTER)  
        return
 
    def find_dropdown(self,driver, browse):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for search suggestion dropdown")  
        try:         
            time.sleep(3)   
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div')
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Found search suggestion dropdown")   
        except (NoSuchElementException):  
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail Search suggestion dropdown not found")    
            driver.quit()
            sys.exit(1)     

    def find_a_suggestion(self,driver, browse):
        """ Now that we've found the dropdown, it seems reasonable there should be at least one suggestion in the list"""    
        logging.info(f"{datetime.now(tz=None)} Search {browse} Info Looking for one search suggestion") 
        try:            
            elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/div/ul')
            logging.info(f"{datetime.now(tz=None)} Search {browse} Info Found one search suggestion")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail Search suggestion not found")    
            driver.quit()
            sys.exit(1)  

    def verify_new_url(self, driver, new_url, browse):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(3) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#                       
        if driver.current_url == new_url:              
            logging.info(f"{datetime.now(tz=None)} Search {browse} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} Search {browse} Fail with {driver.current_url}")           
        return driver  

    def tearDown(self, driver):         
        #driver.close() 
        driver.quit()
        return  

def main():
    """Selenium VERSION 3.141.0
    Task: Create a Selenium test to simulate a search on a website and test that a results page is shown. We can start with the
    SoloSegment.com site search as the first site to test with, but we will eventually create a test that can be used with any of
    our client's sites. Simulate entering a keyword for the letter 's' without pressing enter. Results should be a list of suggestions
    """

    logging.basicConfig(filename='t2search.log', level=logging.INFO)   
    logging.warning("\n")
    url = "https://solosegment.com/"  
    
    #for browse in ["Chrome", "Firefox", "Edge", "Safari", "Ie", "Opera" "Legacy"]:    
    for browse in ["Opera", "Chrome", "Firefox", "Edge","IE"]:
    #for browse in ["Opera"]:    
        mysearch = Search(url)     
        if browse == "Chrome":  
            driver = mysearch.setUpchrome()   # get the handler
        if browse == "Firefox":
            driver = mysearch.setUpfirefox()  # get the handler 
        if browse == "Edge":
            driver = mysearch.setUpedge()     # get the handler
        if browse == "IE":
            driver = mysearch.setUpIE()       # get the handler
        if browse == "Opera":
            driver = mysearch.setUpOpera()    # get the handler

        driver= mysearch.get_the_page(driver, url, browse)         # get the page we want to test
        mysearch.simulate_single_letter_search(driver, 's', browse)    
        mysearch.find_dropdown(driver, browse)
        mysearch.find_a_suggestion(driver, browse) 
        new_url = f"{url}?s=s"
        driver = mysearch.verify_new_url(driver, new_url, browse)     
        mysearch.tearDown(driver)  


if __name__ == "__main__":
    main()
