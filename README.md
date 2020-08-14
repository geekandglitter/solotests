# solotests
Selenium playback testing 

Browser compatability testing for solosegment.com using Selenium playback

t6search.py: runs the two original searches which are search enter and search icon
t5search.py: runs the three newer searchs which are simulate keyword entry, find dropdown, and find search suggestions
maininterfacer.py: the parent class that manages handler setup based on running browser, running platform, and selenium version
note: on MacOS, since Catalina update, notarization has made driver setup a little more complex. See their documentation for more information

 

This information is becoming a little back-level, but here's my blog about these scripts:
https://speakingpython.blogspot.com/2020/07/working-with-selenium-webdriver-in.html (Part One)
https://speakingpython.blogspot.com/2020/07/browser-compatability-testing-with.html (Part Two)
