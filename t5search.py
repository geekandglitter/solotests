#!
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
import platform # To determne which OS platform we're running on

# Selenium Imports
from selenium import webdriver # The webdriver class connects to the browser's instance
from selenium.webdriver.common.keys import Keys  # The Keys class lets you emulate the stroke of keyboard keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

# Relative imports
from maininterfacer import MainInterfacer # Maininterfacer is the base class of WebPage. It manages browser setup.
 
 



class WebPage(MainInterfacer):     # This is the derived class       

    def __init__(self,config, browse):
        super().__init__(config,browse)          
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
        
    
    def simulation(self, message, xpath):
        """Find the search box and type in a single keyword which will force a dropdown"""
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for {message}")
        #time.sleep(10)
        try:   
            elem = WebDriverWait(self.handler, 10).until(            
                EC.presence_of_element_located((By.XPATH, xpath)) # We are looking inside the home session
            )        
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} {message} found")
        except:
            logging.info(f"{datetime.now(tz=None)} Fail {self.browse} {message} not found")    
            self.handler.quit()
            sys.exit(1)
        if message == "search box":    
            elem.send_keys(self.keyword)  
            elem.send_keys(Keys.ENTER)  
        return         

    def verify_results_url(self):       
        """Check on correct url which is https://solosegment.com/?s=solosegment_monitoring_test"""              
        time.sleep(4) # Need this for both Firefox and 
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Checking the results URL")
        if self.handler.current_url == self.results_url:              
            logging.info(f"{datetime.now(tz=None)} {self.browse} Pass")  
        else: 
            logging.info(f"{datetime.now(tz=None)} {self.browse} Fail with {self.handler.current_url} not equal to the expected ur: {self.results_url}")           
        return    

    def tear_down(self):    
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
    if running_platform =="Windows":
        browser_set = ["Firefox", "IE", "Edge", "Chrome"]         
        handler_path = "selenium_deps_windows/drivers/"             
    elif running_platform =="Darwin": # Darwin is a mac
        browser_set=["Firefox", "Safari", "Chrome"]    
        handler_path = "selenium_deps_mac/drivers/"        
    elif running_platform =="Linux":   
        browser_set=["Firefox", "Chrome"]
        handler_path = "selenium_deps_linux/drivers/"
    sel_version = (sys.modules[webdriver.__package__].__version__)[0]     
    
    config = {
        "initial_url": "https://solosegment.com/",
        "results_url": "https://solosegment.com/?s=s",
        "keyword": "s",
        "browser_set": browser_set,            # browser_set depends on which OS is runnng
        "running_platform": running_platform ,            
        "selenium_ver":sel_version,   # detect the version of selenium
        "handler_path": handler_path                
    } 

    """
    #######################################
    # Experiments with json
    import json
    config_str = json.dumps(config)
    print(config_str)
    print(type(config_str))    # string
    config_dict = json.loads(config_str)
    print(config_dict)
    print(type(config_dict))   # dictionary
    with open('data.txt', 'w') as outfile:
        json.dump(config_str, outfile)
    with open('data.txt') as json_file:
        data = json.load(json_file) 
    print(data) 
    print(type(data))          # string
    

    for stuff in config_dict:
        print(stuff, config_dict[stuff])

    for stuff in config_dict.values():
        print(stuff)    

  

    sys.exit(1)  
    ######################################## 

    """





    

    # Our Logger
    logging.basicConfig(filename='t5search.log', level=logging.INFO)  
    logging.info(f"{datetime.now(tz=None)} Info Selenium Version: {sel_version}")        
    logging.info(f"{datetime.now(tz=None)} Info Platform Running: {running_platform}")
    
    for browse in browser_set:                 # we are instantiating a new object each time we start a new browser  
        web_page = WebPage(config, browse)              
        if web_page.handler == None: continue # If the browser handler isn't found, go on to the next browser           
        web_page.start_the_session()          # start the session we want to test
        web_page.simulation("search box", xpath='//*[@id="search-6"]/form/label/input') # simulate keyword entry
        web_page.simulation("search suggestion dropdown", xpath='//*[@id="search-6"]/form/div') # find dropdown 
        web_page.simulation("search suggestions", xpath='//*[@id="search-6"]/form/div/ul') # find search suggestions          
        web_page.verify_results_url()     
        web_page.tear_down()  
    
        
if __name__ == "__main__":
    main()