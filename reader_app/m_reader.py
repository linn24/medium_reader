from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS = json.loads(
    open(dir_path + '/' + 'credentials.json', 'r').read())

# Constant variables
FB_LOGIN_URL = CREDENTIALS['fb_login_url']
READING_LIST_URL = CREDENTIALS['reading_list_url']
CONVERTER_URL = CREDENTIALS['converter_url']
USER_EMAIL = CREDENTIALS['user_email']
USER_PASSWORD = CREDENTIALS['user_password']


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(668, 812)

# Login with Facebook
print('navigating to: ' + FB_LOGIN_URL)
driver.get(FB_LOGIN_URL)
email_field = driver.find_element_by_id("email")
email_field.send_keys(USER_EMAIL)
password_field = driver.find_element_by_id("pass")
password_field.send_keys(USER_PASSWORD)
driver.find_element_by_id("loginbutton").click()

# Wait for 3 seconds for login
time.sleep(3)

# View reading list
print('navigating to: ' + READING_LIST_URL)
driver.get(READING_LIST_URL)

# Wait for 3 seconds
time.sleep(3)

# Close the pop-up
driver.find_element_by_xpath('//button[contains(text(),"Got it")]').click()

# Get all saved articles
elements = driver.find_elements_by_xpath("//a[descendant::h2]")

links = []
for i in range(len(elements)):
    links.append(elements[i].get_attribute('href'))

# Open the first article
print('navigating to: ' + links[0])
driver.get(links[0])

# Remove from bookmark
remove_bookmark_button = driver.find_element_by_xpath('//section//button[@aria-label="Remove Bookmark"]')
remove_bookmark_button.click()

# Get all contents of the article
all_contents = driver.find_element_by_xpath("//article").text

# Go to text-to-speech converter
print('navigating to: ' + CONVERTER_URL)
driver.get(CONVERTER_URL)

# Enter the contents
input_field = driver.find_element_by_id("inputDiv")
input_field.clear()
input_field.send_keys(all_contents)

# Play the reading
play_button = driver.find_element_by_xpath('//app-reader//button[@mattooltip="Play"]')
play_button.click()