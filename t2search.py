# Explanation of delays:
# Implicit waits are used to provide a default waiting time between each consecutive test step/command across the entire test script. 
# Thus, the subsequent test step would only execute when the specified amount of time has elapsed after executing the previous test step/command.
# Explicit waits are used to halt the execution until the time a particular condition is met or the maximum time has elapsed. 
# Unlike Implicit waits, Explicit waits are applied for a particular instance only.
# Implicit Waits are not recommended

# System and Module Imports
import logging 
import sys
from datetime import datetime
import time
import requests
# Selenium Imports
from selenium import webdriver # The webdriver class connects to the browser's instance
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys  # The Keys class lets you emulate the stroke of keyboard keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
# browser Imports
from selenium.webdriver.firefox.options import Options


 


try:
    from msedge.selenium_tools import Edge, EdgeOptions
except:
    pass 
from selenium.webdriver.chrome import service
# browser Imports for Selenium 4
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service # couldn't get Service to work for Edge
from selenium.webdriver.safari.service import Service # untested of course
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Determine which platform
import os
import platform
from pathlib2 import Path # this module lets us consolidate paths across platforms
import os.path
from os import path 
 

class Search():    
          
    selenium_ver = (sys.modules[webdriver.__package__].__version__)[0] # This is how to get the version w/o importing entire package
     
     

    def __init__(self, initial_url, results_url, browse, keyword, running_platform, handler_path):
        self.keyword = keyword
        self.initial_url = initial_url
        self.results_url = results_url
        self.browse=browse
        self.running_platform=running_platform
        self.handler_path = handler_path

        logging.info(f"{datetime.now(tz=None)} Info Looking for {self.browse} browser handler")  
        if self.browse == "Chrome":  
            self.handler = self.set_up_chrome()   # get the handler
        elif browse == "Firefox":
            self.handler = self.set_up_firefox()  # get the handler 
        elif browse == "Edge":
            self.handler = self.set_up_edge()     # get the handler
        elif browse == "IE":
            self.handler = self.set_up_ie()       # get the handler
        elif browse == "Safari":
            self.handler = self.set_up_safari()   # get the handler          
      

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return f"Initial URL is {self.initial_url}\nLanding URL is {self.results_url}"
 
     

    def set_up_chrome(self):
        """Product name: unavailable Product version: unavailable 
        Running Chrome headless with sendkeys requires a window size"""
        options = webdriver.ChromeOptions()           
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless")         

        try:   
            if self.running_platform == "Darwin": # If it's a mac, then use the old API code regardless of Selenium version
                handler = webdriver.Chrome(options=options, executable_path=self.handler_path + 'chromedriver')   
            elif self.running_platform == "Windows" and Search.selenium_ver == "4": # If it's Windows, then check selenium version                
                service = Service(Path(self.handler_path + 'chromedriver.exe')) # Specify the custom path new for Selenium 4                            
                handler = webdriver.Chrome(options=options, service=service)                    
            elif self.running_platform == "Windows": 
                print("executable_path is", Path(self.handler_path + 'chromedriver.exe'))
                handler = webdriver.Chrome(options=options,executable_path=Path(self.handler_path + 'chromedriver.exe')) 

            else: # In case it's Unix
                handler = webdriver.Chrome(options=options,executable_path=Path(self.handler_path +'chromedriver'))    
            logging.info(f"{datetime.now(tz=None)} Info Chrome browser handler found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Info Chrome browser handler not available or failed to launch.")  
            handler = None  
        return handler         

    def set_up_firefox(self):
        """Product name: Firefox Nightly Product version: 71.0a1 
        Firefox can run headless with sendkeys. (Firefox handler is called GeckoDriver)
        Note about firefox driver on MacOS: if it fails to load there's a simple one-time workaround: 
        https://firefox-source-docs.mozilla.org/testing/geckodriver/Notarization.html"""  
        options = Options()
        options.headless = True
                
        try:
            if self.running_platform=="Darwin": # If it's a mac, then use the old API code regardless of Selenium version
                handler = webdriver.Firefox(options=options,executable_path= self.handler_path +'geckodriver')  
            elif self.running_platform == "Windows" and Search.selenium_ver == "4": # If it's Windows, then check selenium version
                service = Service(Path(self.handler_path +'geckodriver.exe')) # Specify the custom path (new for Selenium 4)                
                handler = webdriver.Firefox(options=options, service=service)               
            elif self.running_platform == "Windows":     
                handler = webdriver.Firefox(options=options,executable_path=Path(self.handler_path +'geckodriver.exe')  )
            else: # In case it's Unix
                handler = webdriver.Firefox(options=options,executable_path=Path(self.handler_path +'geckodriver')  )      
            logging.info(f"{datetime.now(tz=None)} Info Firefox browser handler found")             
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Info Firefox browser handler not available or failed to launch.")    
            handler = None    
        return handler            
                

    def set_up_edge(self):
        """Product name: Microsoft WebDriver Product version 83.0.478.58 
        * Edge gets wordy when it's headless, but at least it's working (by setting window size)
        * At the time of this refactor for Selenium 4, Edge does not yet support the new API, so I'm using the legacy one"""  
        options = EdgeOptions()
        options.use_chromium = True          
        #EdgeOptions.AddArguments("headless")  # this version of selenium doesn't have addarguments for edge
        options.headless = True # I got this to work by setting the handler window size  
          
        try:        
            handler = Edge(executable_path=Path(self.handler_path +'msedgedriver.exe'), options = options)   
            handler.set_window_size(1600, 1200)  # set the browser handler window size so that headless will work with sendkeys   
            logging.info(f"{datetime.now(tz=None)} Info Edge browser handler found")     
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail Edge browser handler not available or failed to launch.")    
            handler = None                       
        return handler # ignore the handshake errors  


    def set_up_safari(self): # this Selenium (3) legacy API code works with both selenium 3 and selenium 4
        try:
            handler = webdriver.Safari (executable_path=self.handler_path +'safaridriver')
            handler.maximize_window() # necessary for sendkeys to work           
            logging.info
            (f"{datetime.now(tz=None)} Info Safari browser handler found")
        except:
            logging.info(f"{datetime.now(tz=None)} Fail Safari browser handler not available or failed to launch.")    
            handler = None      
        return handler 


    def set_up_ie(self):
        """Product name: Selenium WebDriver Product version: 2.42.0.0        
        IE does not have support for a headless mode
        IE has some other gotchas, too, which I posted in my blog. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """    
        try:  
            if Search.selenium_ver == "4":
                # for IE, we use the IEDriverServer which might be why it redirects (see log)
                service = Service(Path(self.handler_path +'IEDriverServer.exe')) # Specify the custom path (new for Selenium 4)  
                handler = webdriver.Ie(service=service)  
                logging.info(f"{datetime.now(tz=None)} Finished handler setup")                  
            else:
                handler = webdriver.Ie(executable_path = Path(self.handler_path +'IEDriverServer.exe') )                
             
            handler.maximize_window()
            logging.info(f"{datetime.now(tz=None)} Info IE browser handler found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Fail IE browser handler not available or failed to launch.")    
            handler = None      
        return handler    

   
    def start_the_session(self): # This is where we load the website into the browser
        """See if the website is up and then get the session"""
        try:   
            resp = requests.get(self.initial_url)  # First make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} Info Looking for URL {self.initial_url}")
            if resp.status_code == 200:                
                self.handler.get(self.initial_url) # Now load the website                               
                logging.info(f"{datetime.now(tz=None)} Info URL {self.initial_url} found") 
                logging.info(f"{datetime.now(tz=None)} Info Session Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} Fail URL {self.initial_url} not found. Process terminated")    
            self.handler.quit()
            sys.exit(1)  
        import selenium
         

    def simulate_keyword_entry(self):
        """Find the search box and type in a single keyword which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info Looking for search box")
        try:   
            elem = WebDriverWait(self.handler, 10).until(            
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/label/input')) # We are looking inside the home session
            )        
            logging.info(f"{datetime.now(tz=None)} Info Search box found")
        except:
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
            elem=WebDriverWait(self.handler, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/div'))
            )    
            logging.info(f"{datetime.now(tz=None)} Info Found search suggestion dropdown")   
        except:  
            logging.info(f"{datetime.now(tz=None)} Fail Search suggestion dropdown not found")    
            self.handler.quit()
            sys.exit(1)     
        return    

    def find_search_suggestions(self):
        """Finding one search suggestion is enough evidence that the dropdown is correct"""    
        logging.info(f"{datetime.now(tz=None)} Info Looking for search suggestions") 
        try:            
            elem=WebDriverWait(self.handler, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/div/ul'))
            )    
            logging.info(f"{datetime.now(tz=None)} Info Found search suggestions")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} Fail Search suggestions not found")    
            self.handler.quit()
            sys.exit(1)  
        return    

    def verify_results_url(self):    # might need a webdriverwait until in here because of firefox   
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""              
        time.sleep(4) # Need this for both Firefox and Safari
        if self.handler.current_url == self.results_url:              
            logging.info(f"{datetime.now(tz=None)} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} Fail with {self.handler.current_url} not equal to the expected ur: {self.results_url}")           
        return    

    def tearDown(self):    
        self.handler.quit()
        return

def main():
    """Selenium VERSION 4.0.0 Alpha 5 -- In Version 4 of Selenium, PhantomJS and Opera are no longer supported.
    Task: Create a Selenium test to simulate a search on a website and test that a results session is shown. Simulate entering a keyword for the keyword 's' without pressing enter. Results should be a list of suggestions
    About this script: https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
    """

    logging.basicConfig(filename='t2search.log', level=logging.INFO)     
    logging.info('\n')   
    initial_url = "https://solosegment.com/" 
    results_url = f"{initial_url}?s=s" #class attribute
    keyword = "s"     
    running_platform = platform.system()    
    if running_platform =="Windows":             
        handler_path = "selenium_deps_windows/drivers/"                    
    elif running_platform =="Darwin": # Darwin is a mac           
        handler_path = "selenium_deps_mac/drivers/"        
    elif running_platform =="Linux":           
        handler_path = "selenium_deps_linux/drivers/"  
    else:    
        logging.info(f"{datetime.now(tz=None)} {running_platform} not supported")  
        sys.exit(1)   
    if not path.exists(handler_path):
        logging.info(f"{datetime.now(tz=None)} {handler_path} not found")  
        sys.exit(1)     




    browser_set = ["Chrome", "Firefox", "Safari", "Edge","IE"]   
    for browse in browser_set:                   
        mysearch = Search(initial_url, results_url, browse, keyword, running_platform, handler_path)              
        if mysearch.handler == None: # In the event that the handler is not found or failed to launch,
            continue # go on to the next browser rd   
        mysearch.start_the_session()          # start the session we want to test
        mysearch.simulate_keyword_entry()    
        mysearch.find_dropdown()
        mysearch.find_search_suggestions()
        mysearch.verify_results_url()     
        mysearch.tearDown()  
    logging.info('\n')
        
if __name__ == "__main__":
    main()