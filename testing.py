from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import yaml
import time

# Set up Chrome options
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

# Load the updated YAML file
with open('lab_data.yaml', 'r') as file:
    actions = yaml.safe_load(file)

def perform_action(element):
    locator_strategy = element['locator_strategy']
    locator_value = element['locator_value']
    action = element['action']
    value = element.get('value')

    try:
        if locator_strategy == 'id':
            web_element = driver.find_element(By.ID, locator_value)
        elif locator_strategy == 'xpath':
            web_element = driver.find_element(By.XPATH, locator_value)
        # Add more locator strategies if needed
    except NoSuchElementException:
        print(f"Element not found: {locator_value}")
        return

    # Perform actions on the web element
    if action == 'input':
        web_element.send_keys(value)
    elif action == 'click':
        try:
            # Use WebDriverWait to wait for the element to be clickable before clicking
            wait = WebDriverWait(driver, 10)
            web_element = wait.until(EC.element_to_be_clickable((By.XPATH, locator_value)))
            web_element.click()
        except TimeoutException:
            print(f"Element not clickable: {locator_value}")

# Load the website
driver.get('https://remote-labs.in')

# Perform the actions specified in the YAML file
for action in actions:
    perform_action(action)
    time.sleep(2)

# Close the browser
driver.quit()
