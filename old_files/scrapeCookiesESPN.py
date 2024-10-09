from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver (make sure to have the correct driver installed for your browser)
driver = webdriver.Chrome()

# Navigate to the ESPN Fantasy Football page
driver.get("https://www.espn.com/fantasy/football")

# Wait until the 'espn_s2' cookie is present
try:
    # Wait for up to 5 minutes (300 seconds) for the 'espn_s2' cookie to appear
    WebDriverWait(driver, 300).until(lambda d: driver.get_cookie("espn_s2") is not None)
    print("Logged in successfully and 'espn_s2' cookie is present.")
except:
    print("Timeout: 'espn_s2' cookie not found. Please ensure you are logged in.")
    driver.quit()
    exit()

# Retrieve all cookies after logging in
cookies = driver.get_cookies()

# Convert cookies into a format usable by requests
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

print(driver.get_cookie('SWID')['value'])
print(driver.get_cookie('espn_s2')['value'])

# Print the cookies to use them in requests
print(cookies_dict)

# Option to keep the browser open or close
close_browser = input("Press 'q' to quit the browser or any other key to keep it open: ")
if close_browser.lower() == 'q':
    driver.quit()