import os
os.environ['DISPLAY'] = ':99'
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.common.action_chains import ActionChains
import cv2
import numpy as np
from PIL import Image
from email.message import EmailMessage
import ssl
import smtplib
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from email.message import EmailMessage
import subprocess
import datetime
import imagehash
from dotenv import load_dotenv
from skimage.metrics import structural_similarity as ssim

# timestamps.py
move = 0
timestamps = []
d_movement = ""

def update_timestamps(new_timestamp):
    global timestamps
    timestamps.append(new_timestamp)



load_dotenv()
total = 0
 # Set webdriver options

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Load the updated YAML file
with open('lab_data.yaml', 'r') as file:
    actions = yaml.safe_load(file)


def process_video_frames(driver: webdriver.Chrome, video_xpath: str):
    global move
    screenshot_paths = []
    total_screenshots, interval = 10, 0.5
    video_element = driver.find_element(By.XPATH, video_xpath)

    for i in range(total_screenshots):
        video_screenshot = video_element.screenshot_as_png
        update_timestamps(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if move == 0:
            screenshot_file = f"moving_down_lab/screenshot_{i}.png"
        else:
            screenshot_file = f"moving_up_lab/screenshot_{i}.png"

        with open(screenshot_file, "wb") as file:
            file.write(video_screenshot)

        screenshot_paths.append(screenshot_file)
        time.sleep(interval)
    move += 1
    print(timestamps)
    print("detecting motion")
    

def send_email(person, body, email_subject):
    email_sender = 'rtllab55@gmail.com'
    email_password = 'evyvskiyltlczpaj'
    email_receiver = person
    msg = EmailMessage()
    msg.set_content(body)

    # Set the email parameters
    msg['Subject'] = 'RTL issue'
    msg['From'] = email_sender
    msg['To'] = ', '.join(recipients)  # Join the list of recipients
    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())

def handle_prompt(prompt_text, email_recipient=None, email_subject=None):
    if prompt_text == "Experiment is currently offline":
        body = "Experiment is currently offline"
        if email_recipient and email_subject:
            recipients = ["nageshwalchtwar257@gmail.com", "vedant.nipane@students.iiit.ac.in","rishabh.agrawal@students.iiit.ac.in","abhinav.marri@research.iiit.ac.in"]
            send_email(recipients , body, email_subject)
        try:
            driver.switch_to.alert.accept()
        except UnexpectedAlertPresentException:
            pass
        return True  # Set the flag to True indicating prompt is handled
    elif prompt_text == "Experiment is currently in use":
        driver.switch_to.alert.accept()
        return True  # Set the flag to True indicating prompt is handled
    return False  # Return False if prompt is not handled

# Define a function to perform actions on web elements
def perform_action(element):
    global total

    if total == 2:
        value = os.getenv('PASSWORD')
    else:
        value = element.get('value')

    locator_strategy = element['locator_strategy']
    locator_value = element['locator_value']
    action = element['action']

    try:
        if locator_strategy == 'id':
            time.sleep(10)
            web_element = driver.find_element(By.ID, locator_value)
        elif locator_strategy == 'xpath':
            # time.sleep(5)
            web_element = driver.find_element(By.XPATH, locator_value)
        elif locator_strategy == 'vr':
            pass
        # Add more locator strategies if needed
    except NoSuchElementException:
        web_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Exit Experiment')]")
        web_element.click()
        # # print(list(web_element))
        print(f"Element not found: {locator_value}")
        return

    # Perform actions on the web element
    if action == 'input':
        web_element.send_keys(value)
    elif action == 'click':
        time.sleep(5) 
        # if(len(list(web_element)) >= 3):
        #     web_element[2].click()
        # else:
        if locator_value == "//*[contains(text(), 'Move Down')]" :
            global d_movement
            d_movement = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("Time d_movement : ",d_movement)
            web_element.click()
        elif locator_value == "Vanishing Rod":
            script = """
            var parentDiv = document.querySelector(".-mt-12");
            parentDiv.style.opacity = '1';
            parentDiv.scrollIntoView(true);
            """
            driver.execute_script(script)
            time.sleep(3) #nagesh
            button = driver.find_element(By.ID, "Vanishing Rod")
            button.click()
        else:
            web_element.click()

    elif action == 'process_video_frames':
        process_video_frames(driver, locator_value)
    elif action == 'handle_prompt':
        while True:
            time.sleep(10)
            try:
                alert = driver.switch_to.alert
                prompt_text = alert.text
                prompts = element.get('prompts')
                if prompts:
                    for prompt in prompts:
                        if prompt['prompt_text'] == prompt_text:
                            email_recipient = prompt.get('email_recipient')
                            email_subject = prompt.get('email_subject')
                            if handle_prompt(prompt_text, email_recipient, email_subject):
                                exit()
                                break  # Break out of the inner loop if prompt is handled
                    else:
                        break  # Break out of the outer loop if prompt is not handled
                else:
                    break  # Break out of the outer loop if no prompts are specified
            except NoAlertPresentException:
                break  # Break out of the outer loop if no alert is present

# Load the website
driver.get('https://remote-labs.in')
# Perform the actions specified in the YAML file
time.sleep(3)
for action in actions:
    print(action)
    if total <= 1:
        total += 1
    perform_action(action)
    time.sleep(2)
