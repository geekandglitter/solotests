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
#from selenium.webdriver.chrome.options import Options as CO
#from selenium.webdriver.firefox.options import Options as FO
#from selenium.webdriver.ie.options import Options as IO
#from selenium.webdriver.safari.options import Options as SO 
#from selenium.webdriver.edge.options import Options as EO  

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
from selenium.webdriver.safari.service import Service  
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Determine which platform
import os
import platform
from pathlib2 import Path # this module lets us consolidate paths across platforms
import os.path
from os import path 
 

class WebPage():        
     

    def __init__(self,config, browse):
        self.browse= browse
        
        self.initial_url = config["initial_url"]
        self.results_url = config["results_url"]
        self.keyword = config["keyword"]        
        self.running_platform=config["running_platform"]
        self.selenium_ver = config["selenium_ver"]
        self.handler_path = config["handler_path"]
        logging.info(f"{datetime.now(tz=None)} Info {self.browse} Looking for browser handler")  
        """
        if self.browse == "Chrome":  
            self.handler = self.setUpchrome()   # get the handler
        elif browse == "Firefox":
            self.handler = self.setUpfirefox()  # get the handler 
        elif browse == "Edge":
            self.handler = self.setUpedge()     # get the handler
        elif browse == "IE":
            self.handler = self.setUpIE()       # get the handler
        elif browse == "Safari":
            self.handler = self.setUpsafari()   # get the handler  
        """         
         
        
        # I tried putting in the dict values without quotes and without parens, but Python thinks they're variables.
        # I tried putting the dict values without quotes but with parens, but Python executes them in realtime
        # I tried literal_eval but got a node error
        # I tried literal_eval with the extra quotes trick but then it failed later in the script
        # So I have settled on eval. There has got to be a way.
        browse_config = {
            "Chrome": "self.SetUpChrome()", 
            "Firefox": "self.SetUpFirefox()",
            "Edge": "self.SetUpEdge()",
            "IE": "self.SetUpIE()",
            "Safari": "self.SetUpSafari()"    
        }
         
        self.handler = eval(browse_config[self.browse]) # Literal_eval doesn't work, and I could find no other way
         
        
       
      

    def __repr__(self):
        """This returns better information for the developer when he tries printing the instance"""
        return f"Initial URL is {self.initial_url}\nLanding URL is {self.results_url}"
 
     

    def SetUpChrome(self):
        """Product name: unavailable Product version: unavailable 
        Running Chrome headless with sendkeys requires a window size"""
        options = webdriver.ChromeOptions()           
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless")         

        try:   
            if self.running_platform == "Darwin": # If it's a mac, then use the old API code regardless of Selenium version
                handler = webdriver.Chrome(options=options, executable_path=self.handler_path + 'chromedriver')   
            elif self.running_platform == "Windows" and self.selenium_ver == "4": # If it's Windows, then check selenium version                
                service = Service(Path(self.handler_path + 'chromedriver.exe')) # Specify the custom path new for Selenium 4                            
                handler = webdriver.Chrome(options=options, service=service)                    
            elif self.running_platform == "Windows":                  
                handler = webdriver.Chrome(options=options,executable_path=Path(self.handler_path + 'chromedriver.exe')) 

            else: # In case it's Unix
                handler = webdriver.Chrome(options=options,executable_path=Path(self.handler_path +'chromedriver'))    
            logging.info(f"{datetime.now(tz=None)} Info  {self.browse} browser handler found")  
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Warning  {self.browse} browser handler not found or failed to launch.")  
            handler = None  
        return handler         

    def SetUpFirefox(self):
        """Product name: Firefox Nightly Product version: 71.0a1 
        Firefox can run headless with sendkeys. (Firefox handler is called GeckoDriver)
        Note about firefox driver on MacOS: if it fails to load there's a simple one-time workaround: 
        https://firefox-source-docs.mozilla.org/testing/geckodriver/Notarization.html"""  
        options = Options()
        options.headless = True
                
        try:
            if self.running_platform=="Darwin": # If it's a mac, then use the old API code regardless of Selenium version
                handler = webdriver.Firefox(options=options,executable_path= self.handler_path +'geckodriver')  
            elif self.running_platform == "Windows" and self.selenium_ver == "4": # If it's Windows, then check selenium version
                service = Service(Path(self.handler_path +'geckodriver.exe')) # Specify the custom path (new for Selenium 4)                
                handler = webdriver.Firefox(options=options, service=service)               
            elif self.running_platform == "Windows":     
                handler = webdriver.Firefox(options=options,executable_path=Path(self.handler_path +'geckodriver.exe')  )
            else: # In case it's Unix
                handler = webdriver.Firefox(options=options,executable_path=Path(self.handler_path +'geckodriver')  )      
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} browser handler found")             
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Warning {self.browse} browser handler not found or failed to launch.")    
            handler = None    
        return handler            
                

    def SetUpEdge(self):
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
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} browser handler found")     
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Warning {self.browse} browser handler not found or failed to launch.")    
            handler = None                       
        return handler # ignore the handshake errors  


    def SetUpSafari(self): # this Selenium (3) legacy API code works with both selenium 3 and selenium 4
        try:
            handler = webdriver.Safari (executable_path=self.handler_path +'safaridriver')
            handler.maximize_window() # necessary for sendkeys to work           
            logging.info
            (f"{datetime.now(tz=None)} Info {self.browse} browser handler found")
        except:
            logging.info(f"{datetime.now(tz=None)} Warning {self.browse} browser handler not found or failed to launch.")    
            handler = None      
        return handler 


    def SetUpIE(self):
        """Product name: Selenium WebDriver Product version: 2.42.0.0        
        IE does not have support for a headless mode
        IE has some other gotchas, too, which I posted in my blog. 
        See https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html
        """    
        try:  
            if self.selenium_ver == "4":
                # for IE, we use the IEDriverServer which might be why it redirects (see log)
                service = Service(Path(self.handler_path +'IEDriverServer.exe')) # Specify the custom path (new for Selenium 4)  
                handler = webdriver.Ie(service=service)  
                logging.info(f"{datetime.now(tz=None)} Info {self.browse} Finished handler setup")                  
            else:
                handler = webdriver.Ie(executable_path = Path(self.handler_path +'IEDriverServer.exe') )                
             
            handler.maximize_window()
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} browser handler found") 
        except (WebDriverException):
            logging.info(f"{datetime.now(tz=None)} Warning {self.browse} browser handler not found or failed to launch.")    
            handler = None      
        return handler    

   
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

    def verify_results_url(self):    # might need a webdriverwait until in here because of firefox   
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

    logging.basicConfig(filename='t3search.log', level=logging.INFO)     
    logging.info('\n')       
 
    running_platform = running_platform = platform.system()         
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