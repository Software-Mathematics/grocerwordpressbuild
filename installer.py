import os
import time

from progress.bar import ChargingBar
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# defining all the variables
ChargingBar = ChargingBar('Processing', max=68)
default_timeout = 400  # 300 seconds
duplicator_dir = "./"

grocer_url = "http://185.207.250.107"


"""
Enter sudo password to continue script running needed for smoothly running docker and changing the permissions of files on the mount volume
"""
#sudo_pass = getpass.getpass(prompt='Enter your sudo password:')
ChargingBar.next()

# downloading geckodriver to run selenium
""" 
# not needed as gecko driver will be installed by ansible
gecko_driver_url = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz"
gecko_driver_zip = "geckodriver-v0.31.0-linux64.tar.gz"
os.system(f'rm -rf {gecko_driver_zip}  >> installer.log 2>&1')
os.system(
    f'wget {gecko_driver_url} >> installer.log 2>&1')
os.system('rm -rf geckodriver  >> installer.log 2>&1')
os.system(f'tar -xvf {gecko_driver_zip} >> installer.log 2>&1')
"""
os.system(f'cp {duplicator_dir}/docker-compose.yml ./ >> installer.log 2>&1')
ChargingBar.next()

# Running the docker containers
os.system('docker-compose up -d >> installer.log 2>&1')
for i in range(30):
    ChargingBar.next()
    time.sleep(1)
#os.system('echo %s|sudo -S %s' % (sudo_pass, 'rm -rf httpd/*'))
os.system(f'cp {duplicator_dir}/installer.php ./httpd/ >> installer.log 2>&1')
os.system(f'cp {duplicator_dir}/20220802_grocery_85474e13dfd57eb02214_20220802061632_archive.zip ./httpd/ >> installer.log 2>&1')
#os.system('docker-compose down >> installer.log 2>&1')
os.system(f'chown -R www-data:www-data httpd/ >> installer.log 2>&1')
ChargingBar.next()
#os.system('docker-compose up -d >> installer.log 2>&1')
#time.sleep(10)
ChargingBar.next()




# starting selenium as a headless mode
options = FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)
for i in range(5):
    ChargingBar.next()
    time.sleep(1)
browser.get(f'{grocer_url}/installer.php')
ChargingBar.next()
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
    print("Page 1 loading took too much time!")
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
    print("Page 2 loading too much time!")
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
    print("Page 3 loading took too much time!")

timeout = 100
try:
    ok_button = EC.presence_of_element_located((By.ID, 'db-install-dialog-confirm-button'))
    WebDriverWait(browser, timeout).until(ok_button)
    ok_button = browser.find_element(By.ID, 'db-install-dialog-confirm-button')
    ok_button.send_keys(Keys.RETURN)
    for i in range(45):
        ChargingBar.next()
        time.sleep(1)
except TimeoutException:
    print("Page 1 loading took too much time!")
ChargingBar.finish()
print(f"Grocer has been successfully installed.!!!\nNow you can open URL : {grocer_url} in your browser and use it")