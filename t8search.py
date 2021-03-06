#!
import logging
import sys
from datetime import datetime
import requests
# Selenium Imports
from selenium import webdriver # The webdriver class connects to the browser's instance
from selenium.webdriver.common.keys import Keys  # The Keys class lets you emulate the stroke of keyboard keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import platform # To determne which OS platform we're running on
from maininterfacer import MainInterfacer # Maininterfacer is the base class of WebPage. It manages browser setup.
import time
import json
 


class WebPage(MainInterfacer):       # This is the derived class     

    def __init__(self, browse, sel_ver, running_platform):
        super().__init__(browse, sel_ver, running_platform)   
        self.initial_url="https://solosegment.com/"
        self.results_url="https://solosegment.com/?s=solo_search"
        self.keyword= "solo_search"      
        #logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for browser handler")
         
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
        
    
    def simulate_search_enter(self, message, xpath):
        """Find the search box and type in a single keyword which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for {message}")
         
        try:   
            elem = WebDriverWait(self.handler, 10).until(            
                EC.presence_of_element_located((By.XPATH, xpath)) # We are looking inside the home session
            )        
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} {message} found")
        except:
            logging.info(f"{datetime.now(tz=None)} Fail {self.browse} {message} not found")    
            self.handler.quit()
            sys.exit(1)
        elem.click() 
        elem.send_keys(self.keyword)  
        elem.send_keys(Keys.ENTER)  
        return     

    def simulate_search_icon(self, message, xpath):   
        """Find the search box and type in a single keyword which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for {message}")
         
        try:   
            elem = WebDriverWait(self.handler, 10).until(            
                EC.presence_of_element_located((By.XPATH, xpath)) # We are looking inside the home session
            )        
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} {message} found")
        except:
            logging.info(f"{datetime.now(tz=None)} Fail {self.browse} {message} not found")    
            self.handler.quit()
            sys.exit(1)
        elem.clear() # We are running this test on the search results page, so clear the text box first
        elem.send_keys(self.keyword) 
        elem=self.handler.find_element(By.XPATH, '//*[@id="search-6"]/form/input')
        webdriver.ActionChains(self.handler).move_to_element(elem).perform()  # perform moves the mouse now     
        elem.click()          
        return          

    def verify_results_url(self):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""              
        time.sleep(4) # Need this for both Firefox and Safari 
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Checking the results URL")
        if self.handler.current_url == self.results_url:              
            logging.info(f"{datetime.now(tz=None)} {self.browse} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} {self.browse} Fail with {self.handler.current_url} not equal to the expected url: {self.results_url}")           
        return    

    def tear_down(self):    
        self.handler.set_page_load_timeout(20) # This helps prevent Error reading broker pipe 
        self.handler.quit()
        return

def main():
    """Selenium VERSION 4.0.0 Alpha 5 -- In Version 4 of Selenium, PhantomJS and Opera are no longer supported.
    This script runs three simulations
    1. Simulate a keyword entry ('s') without pressing enter
    2. Locate the dropdown
    3. Find a search suggestion in the dropdown 
    """
 
    # Our Configs
    running_platform = platform.system()    # Which OS are we running on?         
    sel_ver = (sys.modules[webdriver.__package__].__version__)[0] 
     
    with open('test_config.txt') as json_file:
        data = json.load(json_file) 
        config = json.loads(data)

    # Our logger
    logging.basicConfig(filename='t8search.log', level=logging.INFO) 
    logging.info(f"{datetime.now(tz=None)} Info Selenium Version: {sel_ver}")        
    logging.info(f"{datetime.now(tz=None)} Info Platform Running: {running_platform}")


    for browser_select in  config [running_platform]["browser_set"]:                 # we are instantiating a new object each time we start a new browser  
                
        web_page = WebPage(browser_select, sel_ver, running_platform)             
        if web_page.handler == None: continue # If the browser handler isn't found, go on to the next browser           
        web_page.start_the_session()          # start the session we want to test, then simulate keyword entry
        web_page.simulate_search_enter("Search box for ENTER simulation", xpath='//*[@id="search-6"]/form/label/input') 
        web_page.simulate_search_icon("Search box for ICON simulation", xpath='//*[@id="search-6"]/form/label/input' )           
        web_page.verify_results_url()     
        web_page.tear_down()  
    
        
if __name__ == "__main__":
    main()