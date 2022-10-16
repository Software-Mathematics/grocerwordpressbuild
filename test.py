from selenium import webdriver  
from selenium.webdriver.firefox.options import Options
#binary = FirefoxBinary('/root/Downloads/firefox/firefox')  
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
#driver = webdriver.Firefox()  
driver.get('http://localhost/installer.php')
# insert time.sleep() here  
driver.close()
