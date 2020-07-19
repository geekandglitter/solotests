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
# browser Imports
from selenium.webdriver.firefox.options import Options
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome import service
# browser Imports for Selenium 4
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service # couldn't get Service to work for Edge
from selenium.webdriver.safari.service import Service # untested of course
from selenium.webdriver.ie.service import Service

 

class Search():    
    test_name = "Search 3" #class attribute       

    def __init__(self, initial_url, results_url, browse, keyword):
        self.keyword = keyword
        self.initial_url = initial_url
        self.results_url = results_url
        self.browse=browse
        if browse == "Chrome":  
            handler = self.setUpchrome()   # get the handler
        elif browse == "Firefox":
            handler = self.setUpfirefox () # get the handler 
        elif browse == "Edge":
            handler = self.setUpedge()     # get the handler
        elif browse == "IE":
            handler = self.setUpIE()       # get the handler
        elif browse == "Safari":
            handler = self.setUpsafari()   # get the handler
        self.handler=handler
      

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return f"Initial URL is {self.initial_url}\nLanding URL is {self.results_url}"
 
     

    def setUpchrome(self):
        """Product name: unavailable Product version: unavailable 
        Running Chrome headless with sendkeys requires a window size"""
        options = webdriver.ChromeOptions()           
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless") 
        logging.info(f"{datetime.now(tz=None)} Info Looking for Chrome browser handler")  

        try:
            service = Service('selenium_deps\\drivers\\chromedriver.exe') # Specify the custom path (new for Selenium 4)            
            handler = webdriver.Chrome(options=options, service=service)   
            logging.info(f"{datetime.now(tz=None)} Info Chrome browser handler found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Chrome browser handler not found or failed to launch.")    
            handler = None  
        return handler         

    def setUpfirefox(self):
        """Product name: Firefox Nightly Product version: 71.0a1 
        Firefox can run headless with sendkeys. (Firefox handler is called GeckoDriver)"""  
        options = Options()
        options.headless = True
        logging.info(f"{datetime.now(tz=None)} Info Looking for Firefox browser handler") 
        
        try:
            service = Service('selenium_deps\\drivers\\geckodriver.exe') # Specify the custom path (new for Selenium 4)
            handler = webdriver.Firefox(options=options, service=service)
            logging.info(f"{datetime.now(tz=None)} Info Firefox browser handler found")             
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Firefox browser handler not found or failed to launch.")    
            handler = None    
        return handler      

    def setUpedge(self):
        """Product name: Microsoft WebDriver Product version 83.0.478.58 
        * Edge gets wordy when it's headless, but at least it's working (by setting window size)
        * At the time of this refactor for Selenium 4, Edge does not yet support the new API, so I'm using the legacy one"""  
        options = EdgeOptions()
        options.use_chromium = True          
        #EdgeOptions.AddArguments("headless")  # this version of selenium doesn't have addarguments for edge
        options.headless = True # I got this to work by setting the handler window size  
        logging.info(f"{datetime.now(tz=None)} Info Looking for Edge browser handler")  
        try:
            handler = Edge(executable_path='selenium_deps\\drivers\\msedgedriver.exe', options = options)   
            handler.set_window_size(1600, 1200)  # set the browser handler window size so that headless will work with sendkeys   
            logging.info(f"{datetime.now(tz=None)} Info Edge browser handler found")     
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Edge browser handler not found or failed to launch.")    
            handler = None                       
        return handler # ignore the handshake errors 


    def setUpsafari(self):
        """I cannot currently test this safari code beause my only ios is on an old ipad Safari 12.4.7.  
        I posted a writeup on implementing Safari that might be of some help. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """ 
        return
        logging.info(f"{datetime.now(tz=None)} Info Looking for Safari browser handler")  
        try:       
            service = Service('selenium_deps\\drivers\\safaridriver.exe') # Specify the custom path (new for Selenium 4)       
            handler = webdriver.Safari(options=options, service=service)    
            logging.info(f"{datetime.now(tz=None)} Info Safari browser handler found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Safari browser handler not found or failed to launch.")    
            handler = None       
        return handler 

    def setUpIE(self):
        """Product name: Selenium WebDriver Product version: 2.42.0.0
        IE does not have support for a headless mode
        IE has some other gotchas, too, which I posted in my blog. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """    
        logging.info(f"{datetime.now(tz=None)} Info Looking for IE browser handler")   
        try:   
            service = Service('selenium_deps\\drivers\\IEDriverServer.exe') # Specify the custom path (new for Selenium 4)  
            handler = webdriver.Ie(service=service)                     
            handler.implicitly_wait(2)
            handler.maximize_window()
            logging.info(f"{datetime.now(tz=None)} Info IE browser handler found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail IE browser handler not found or failed to launch.")    
            handler = None      
        return handler    

   
    def start_the_session(self):
        """See if the session is up and then get the session"""
        try:   
            resp = requests.get(self.initial_url)  # This is how we have to make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} Info Looking for URL {self.initial_url}")
            if resp.status_code == 200:                
                self.handler.get(self.initial_url)
                time.sleep(10)   
                logging.info(f"{datetime.now(tz=None)} Info URL {self.initial_url} found") 
                logging.info(f"{datetime.now(tz=None)} Info Session Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} Fail URL {self.initial_url} not found. Process terminated")    
            self.handler.quit()
            sys.exit(1)                 
        return  

    def simulate_keyword_entry(self):
        """Find the search box and type in a single keyword which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info Looking for search box")
        try:               
            elem=self.handler.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We are looking inside the home session
            logging.info(f"{datetime.now(tz=None)} Info Search box found")
        except (NoSuchElementException):
            logging.info(f"{datetime.now(tz=None)} Fail Search box not found")    
            self.handler.quit()
            sys.exit(1)
        elem.send_keys(self.keyword)  
        elem.send_keys(Keys.ENTER)  
        return
 
    def find_dropdown(self):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info Looking for search suggestion dropdown")  
        try:         
            time.sleep(3)   
            elem=self.handler.find_element(By.XPATH, '//*[@id="search-6"]/form/div')
            logging.info(f"{datetime.now(tz=None)} Info Found search suggestion dropdown")   
        except (NoSuchElementException):  
            logging.info(f"{datetime.now(tz=None)} Fail Search suggestion dropdown not found")    
            self.handler.quit()
            sys.exit(1)     
        return    

    def find_search_suggestions(self):
        """Finding one search suggestion is enough evidence that the dropdown is correct"""    
        logging.info(f"{datetime.now(tz=None)} Info Looking for search suggestions") 
        try:            
            elem=self.handler.find_element(By.XPATH, '//*[@id="search-6"]/form/div/ul')
            logging.info(f"{datetime.now(tz=None)} Info Found search suggestions")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} Fail Search suggestions not found")    
            self.handler.quit()
            sys.exit(1)  
        return    

    def verify_results_url(self):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""  
        time.sleep(4) # Needed this for firefox; otherwise it looks for: https://solosegment.com/#                       
        if self.handler.current_url == self.results_url:              
            logging.info(f"{datetime.now(tz=None)} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} Fail with {self.handler.current_url} not equal to the expected ur: {self.results_url}")           
        return    

    def tearDown(self):    
        self.handler.quit()
        return

def main():
    """Selenium VERSION 4.0.0 Alpha 5 -- In this version, PhantomJS and Opera are no longer supported
    Task: Create a Selenium test to simulate a search on a website and test that a results session is shown. We can start with the
    SoloSegment.com site search as the first site to test with, but we will eventually create a test that can be used with any of
    our client's sites. Simulate entering a keyword for the keyword 's' without pressing enter. Results should be a list of suggestions
    About this script: https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
    """

    logging.basicConfig(filename='t2search.log', level=logging.INFO)      
    initial_url = "https://solosegment.com/" 
    results_url = f"{initial_url}?s=s" #class attribute
    keyword = "s"

    for browse in  [ "Chrome", "Firefox", "Edge","IE"]:      #for browse in  [ "Chrome", "Firefox", "Edge","IE", "Safari"]:           
        mysearch = Search(initial_url, results_url, browse, keyword)     
         
        if mysearch.handler == None: # In the event that the handler is not found or failed to launch,
            continue # go on to the next browser
        mysearch.start_the_session()          # start the session we want to test
        mysearch.simulate_keyword_entry()    
        mysearch.find_dropdown()
        mysearch.find_search_suggestions()
        mysearch.verify_results_url()     
        mysearch.tearDown()  
if __name__ == "__main__":
    main()