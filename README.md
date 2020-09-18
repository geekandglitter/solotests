
### This project performs browser compatability testing for solosegment.com using Selenium playback.  
### Notes
 
1. They work on Selenium 3 and Selenium 4 
2. They work on Mac, Windows, and Linux
3. They work on all browsers supported on your OS platform: Chrome, Firefox, Edge, Safari, IE
4. This project is still under development, but is suitable for use "as is" and for repurposing
5. The project files are:

	- t7search.py
	- t8search.py 
    - maininterfacer.py
    - test_config.txt
    - three webdriver folders containing browser-based webdrivers used by the developer

6. t7search.py runs three searches: simulate keyword entry, find dropdown, and find search suggestions
7. t8search.py runs two searches: search enter and search icon
8. maininterfacer.py: the base class that manages handler setup based on running browser, running platform, and selenium version
9. test_config is the external config file containing the browser set and handler path for each of the 3 OS platforms
10. On MacOS, since Catalina update, notarization has made driver setup a little more complex. See their documentation for more information
11. See requirements.txt for a note about selenium versions
12. Info to get started with selenium: https://pypi.org/project/selenium/4.0.0a6.post1/
13. Webdriver support for Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/ 
14. The drivers supplied here are the ones used most recently by the developer. Choose the webdriver to match each browser for each OS platform for your installation and test environment.
15. See my blog post https://speakingpython.blogspot.com/2020/08/managing-selenium-webdrivers-for-all.html for more considerations specific to OS platform and browser selection. This blog post also contains more general findings as well.