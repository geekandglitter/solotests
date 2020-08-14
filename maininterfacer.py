#!
# System and Module Imports
import logging
from datetime import datetime
# Selenium Imports
from selenium import webdriver # The webdriver class connects to the browser's instance
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
from selenium.webdriver.safari.service import Service  
from selenium.webdriver.ie.service import Service
# Determine which platform
from pathlib2 import Path # this module lets us consolidate paths across platforms
 

class MainInterfacer():
    """ Parent class for selenium webdriver scripts. It does the handler setup based on three factors:
    1. Browser (Firefox, IE, Safari, Edge, Chrome)
    2. Selenium version (could be Selenium 3 or the Selenium 4 beta)
    3. OS Platofrm (Mac, Windows or Linux)
    """
    def __init__(self, config, browse):        
        self.initial_url = config["initial_url"]
        self.results_url = config["results_url"]
        self.keyword = config["keyword"]        
        self.running_platform=config["running_platform"]
        self.selenium_ver = config["selenium_ver"]
        self.handler_path = config["handler_path"]
        self.browse=browse

        self.driverSelect = {
            "Chrome": self.SetUpChrome,          
            "Firefox": self.SetUpFirefox,
            "Edge": self.SetUpEdge,
            "IE": self.SetUpIE,
            "Safari": self.SetUpSafari
        }
        self.handler = self.driverSelect[self.browse]() # Go get Our Handler         


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

            else: # In case it's Linux
                handler = webdriver.Chrome(options=options,executable_path=Path(self.handler_path +'chromedriver'))    
            logging.info(f"{datetime.now(tz=None)} Info {self.browse} browser handler found")  
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
