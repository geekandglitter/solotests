
### This project performs browser compatability testing for solosegment.com using Selenium playback.  
### Notes
 
1. They work on Selenium 3 and Selenium 4 
2. They work on Mac, Windows, and Linux
3. They work on all browsers supported on your OS platform: Chrome, Firefox, Edge, Safari, IE
4. This project is still under development, but is suitable for use "as is" and for repurposing
5. The project files are:

	- t5search.py
	- t6search.py 
    - maininterfacer.py
    - three webdriver folders containing browser-based webdrivers used by the developer

6. t5search.py runs three searches: simulate keyword entry, find dropdown, and find search suggestions
7. t6search.py runs two searches: search enter and search icon
8. maininterfacer.py: the base class that manages handler setup based on running browser, running platform, and selenium version
9. On MacOS, since Catalina update, notarization has made driver setup a little more complex. See their documentation for more information
10. See requirements.txt for a note about selenium versions
11. To get started with selenium: https://pypi.org/project/selenium/4.0.0a6.post1/
12. Webdriver support for Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/ 
13. The drivers supplied here are the ones used by the developer. Choose the webdriver to match each browser for each OS platform.
14. See my blog post https://speakingpython.blogspot.com/2020/08/managing-selenium-webdrivers-for-all.html for considerations specific to OS platform and browser selection. This blog also contains more general findings as well.
 
