import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import getpass
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from progress.bar import Bar, ChargingBar

ChargingBar = ChargingBar('Processing', max=10)
default_timeout = 300 # 300 seconds
home_dir = "/home/devops"
# Enter sudo password to continue script running
sudo_pass = getpass.getpass(prompt='Enter your sudo password:')
os.system('rm -rf geckodriver-v0.31.0-linux64.tar.gz')
ChargingBar.next()
# downloading geckodriver to run selenium
os.system('wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz >> installer.log 2>&1')
os.system('rm -rf geckodriver')
os.system('tar -xvf geckodriver-v0.31.0-linux64.tar.gz >> installer.log 2>&1')
os.system('cp '+home_dir+'/docker-compose.yml ./')
ChargingBar.next()
os.system('docker-compose up -d >> installer.log 2>&1')

os.system('echo %s|sudo -S %s' % (sudo_pass, 'rm -rf httpd/*'))
os.system('echo %s|sudo -S %s' % (sudo_pass, 'cp /home/devops/installer.php ./httpd/ >> installer.log 2>&1'))
os.system('echo %s|sudo -S %s' % (sudo_pass, 'cp /home/devops/20220802_grocery_85474e13dfd57eb02214_20220802061632_archive.zip ./httpd/ >> installer.log 2>&1'))
os.system('docker-compose down >> installer.log 2>&1')
ChargingBar.next()
os.system('docker-compose up -d >> installer.log 2>&1')
time.sleep(10)
ChargingBar.next()
# starting selenium as a headless mode

options = FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)
#options = Options()
#options.headless = True
#browser = webdriver.Firefox(options=options)
time.sleep(30)
browser.get('http://185.207.250.107/installer.php')
ChargingBar.next()
# delay = 3   # seconds
timeout = 100
try:
    elem0 = EC.presence_of_element_located((By.ID, 'param_item_secure-archive'))
    WebDriverWait(browser, timeout).until(elem0)
    elem0 = browser.find_element(By.ID, "param_item_secure-archive")
    elem0.send_keys('20220802_grocery_85474e13dfd57eb02214_20220802061632_archive.zip')
    submit_button = browser.find_element(By.ID, 'secure-btn')
    submit_button.send_keys(Keys.RETURN)
    ChargingBar.next()
except TimeoutException:
    print("Loading took too much time!")
timeout = 1000
try:
    dbhost = EC.presence_of_element_located((By.NAME, 'dbhost'))
    WebDriverWait(browser, timeout).until(dbhost)
    dbhost = browser.find_element(By.NAME, "dbhost")
    dbhost.clear()
    dbhost.send_keys('db')
    dbname = browser.find_element(By.NAME, "dbname")
    dbname.send_keys('exampledb')
    dbuser = browser.find_element(By.NAME, "dbuser")
    dbuser.send_keys('exampleuser')
    dbpass = browser.find_element(By.NAME, "dbpass")
    dbpass.send_keys('examplepass')
    validate_button = browser.find_element(By.ID, 'validate-button')
    validate_button.send_keys(Keys.RETURN)
    ChargingBar.next()
except TimeoutException:
    print("Loading 2 took too much time!")
timeout = 1000
try:
    radio_btn = EC.element_to_be_clickable((By.NAME, 'accept-warnings'))
    WebDriverWait(browser, timeout).until(radio_btn)
    radio_btn = browser.find_element(By.NAME, "accept-warnings")
    radio_btn.click()
    next_button = browser.find_element(By.ID, 's1-deploy-btn')
    next_button.send_keys(Keys.RETURN)
    ChargingBar.next()
except TimeoutException:
    print("Loading 3 took too much time!")

timeout = 100
try:
    ok_button = EC.presence_of_element_located((By.ID, 'db-install-dialog-confirm-button'))
    WebDriverWait(browser, timeout).until(ok_button)
    ok_button = browser.find_element(By.ID, 'db-install-dialog-confirm-button')
    ok_button.send_keys(Keys.RETURN)
    time.sleep(45)
    ChargingBar.next()
    ChargingBar.next()
except TimeoutException:
    print("Loading 4 took too much time!")
ChargingBar.finish()

