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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Determine which platform 
import platform 
from os import path 
from maininterfacer import MainInterfacer # MainInterfacer manages OS platforms

class WebPage(MainInterfacer):            

    def __init__(self,config, browse):
        super().__init__(config,browse)          
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for browser handler")
         
    def __repr__(self):         
        return f"Initial URL is {self.initial_url}\nLanding URL is {self.results_url}"    
   
    def start_the_session(self): # This is where we load the website into the browser
        """See if the website is up and then get the session"""
        try:   
            resp = requests.get(self.initial_url)  # First make sure the URL exists and is obtainable
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for URL {self.initial_url}")
            if resp.status_code == 200:                
                self.handler.get(self.initial_url) # Now load the website                               
                logging.info(f"{datetime.now(tz=None)} Info {self.browse} URL {self.initial_url} found") 
                logging.info(f"{datetime.now(tz=None)} Info {self.browse} Session Initialized") 
        except:             
            logging.info(f"{datetime.now(tz=None)} Fail {self.browse} URL {self.initial_url} not found. Process terminated")    
            self.handler.quit()
            sys.exit(1)  
        import selenium
    
    def simulate_keyword_entry(self):
        """Find the search box and type in a single keyword which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for search box")
        try:   
            elem = WebDriverWait(self.handler, 10).until(            
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/label/input')) # We are looking inside the home session
            )        
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} Search box found")
        except:
            logging.info(f"{datetime.now(tz=None)} Fail {self.browse} Search box not found")    
            self.handler.quit()
            sys.exit(1)
        elem.send_keys(self.keyword)  
        elem.send_keys(Keys.ENTER)  
        return

    def find_dropdown(self):
        """See that we have a search suggestion dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for search suggestion dropdown")  
        time.sleep(10)

        try:         
            elem=WebDriverWait(self.handler, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/div'))
            )    
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} Found search suggestion dropdown")   
        except:  
            logging.info(f"{datetime.now(tz=None)} Fail {self.browse} Search suggestion dropdown not found")    # failing here
            self.handler.quit()
            sys.exit(1)     
        return    

    def find_search_suggestions(self):
        """Finding one search suggestion is enough evidence that the dropdown is correct"""    
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for search suggestions") 
        try:            
            elem=WebDriverWait(self.handler, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-6"]/form/div/ul'))
            )    
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} Found search suggestions")                
        except (NoSuchElementException):             
            logging.info(f"{datetime.now(tz=None)} Fail {self.browse} Search suggestions not found")    
            self.handler.quit()
            sys.exit(1)  
        return    

    def verify_results_url(self):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""              
        time.sleep(4) # Need this for both Firefox and Safari
        if self.handler.current_url == self.results_url:              
            logging.info(f"{datetime.now(tz=None)} {self.browse} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} {self.browse} Fail with {self.handler.current_url} not equal to the expected ur: {self.results_url}")           
        return    

    def tearDown(self):    
        self.handler.quit()
        return

def main():
    """Selenium VERSION 4.0.0 Alpha 5 -- In Version 4 of Selenium, PhantomJS and Opera are no longer supported.
    Task: Create a Selenium test to simulate a search on a website and test that a results session is shown. Simulate entering a keyword for the keyword 's' without pressing enter. Results should be a list of suggestions
    About this script: https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
    """

    logging.basicConfig(filename='t4search.log', level=logging.INFO)     
    logging.info('\n')       
 
    running_platform = platform.system()         
    if running_platform =="Windows":
        browser_set = [ "Firefox", "IE", "Edge", "Chrome"] 
        handler_path = "selenium_deps_windows/drivers/"             
    elif running_platform =="Darwin": # Darwin is a mac
        browser_set=["Firefox", "Safari", "Chrome"]    
        handler_path = "selenium_deps_mac/drivers/"        
    elif running_platform =="Linux":   
        browser_set=["Firefox", "Chrome"]
        handler_path = "selenium_deps_linux/drivers/"      
    
    config = {
            "initial_url": "https://solosegment.com/",
            "results_url": "https://solosegment.com/?s=s",
            "keyword": "s",
            "browser_set": browser_set,            # browser_set depends on which OS is runnng
            "running_platform": platform.system(),            
            "selenium_ver": (sys.modules[webdriver.__package__].__version__)[0],   # detect the version of selenium
            "handler_path": handler_path                
    }   
        
    for browse in browser_set:                 # we are instantiating a new object each time we start a new browser  
        web_page = WebPage(config, browse)              
        if web_page.handler == None: # In the event that the handler is not found or failed to launch,
            continue # go on to the next browser rd   
        web_page.start_the_session()          # start the session we want to test
        web_page.simulate_keyword_entry()    
        web_page.find_dropdown()
        web_page.find_search_suggestions()
        web_page.verify_results_url()     
        web_page.tearDown()  
    logging.info('\n')
        
if __name__ == "__main__":
    main()