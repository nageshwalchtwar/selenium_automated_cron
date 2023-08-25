import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, NoSuchElementException
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
import logging
from logging.handlers import RotatingFileHandler
from skimage.metrics import structural_similarity as ssim
import ss_4_lab
import apparatus_level
#logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='lab_direction.log', filemode='a',format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
# Create a logger
# logger = logging.getLogger('my_logger')
# logger.setLevel(logging.DEBUG)

# # Create a rotating file handler
# handler = RotatingFileHandler('app.log', maxBytes=1024, backupCount=3)

# # Set the log level for the handler
# handler.setLevel(logging.DEBUG)

# # Configure the log format
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# # Add the handler to the logger
# logger.addHandler(handler)
level= apparatus_level.liquid_levels
load_dotenv()
ss_paths = ss_4_lab.ss_paths
print(ss_paths)
def send_email(person, body, email_subject):
    email_sender = 'rtllab55@gmail.com'
    email_password = 'evyvskiyltlczpaj'
    email_receiver = person
    msg = EmailMessage()
    msg.set_content(body)

    # Set the email parameters
    msg['Subject'] = 'RTL - Maintainance update'
    msg['From'] = email_sender
    msg['To'] = ', '.join(recipients)  # Join the list of recipients
    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())

def process_image(image_path1, image_path2):
    # Read the images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # Convert the images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the two grayscale images
    diff = cv2.absdiff(gray1, gray2)

    # Apply a threshold to create a binary image
    threshold = 60  # Adjust the threshold as needed
    _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define the minimum and maximum areas for bounding boxes
    min_area = 100  # Minimum area threshold for bounding boxes
    max_area = 5000  # Maximum area threshold for bounding boxes

    # Store the coordinates of bounding boxes in a list of tuples
    bounding_boxes = []

    # Draw bounding boxes around the contours within the specified area range
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            x, y, w, h = cv2.boundingRect(contour)
            bounding_boxes.append((x, y))
            cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image with filtered bounding boxes
    # cv2.imwrite("Image with Filtered Bounding Boxes", image1) 
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Return the list of bounding boxes
    return bounding_boxes

def compare_images(image1, image2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute the SSIM score
    similarity_score = ssim(gray1, gray2)
    similarity_threshold = 0.98
    if similarity_score >= similarity_threshold:
        return 0
    else:
        return 1
def compare_ss(f_path):
    print("comparing")
    image_path1 = f_path + 'screenshot_0.png'
    image_path2 = f_path + 'screenshot_8.png'

    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)
    
    #diff = last_centroid[1] - first_centroid[1]
    if compare_images(image1, image2) == 0:
        print("still")
        return "still"
    else:
        if f_path == 'moving_down_lab/':
            image_path1,image_path2,image_path3,image_path4 = ss_paths[0:4]
        else:
            image_path1,image_path2,image_path3,image_path4 = ss_paths[4:]
        
        bounding_boxes1 = process_image(image_path1, image_path2)
        bounding_boxes2 = process_image(image_path3, image_path4)
        print("motion")
        sorted_array1 = sorted(bounding_boxes1, key=lambda x: x[0])
        sorted_array2 = sorted(bounding_boxes2, key=lambda x: x[0])

        # Initialize an empty list to store the associations
        associations = []

        # Iterate over each point in the second array
        for point2 in sorted_array2:
            min_distance = 50
            associated_point = None
            
            # Find the closest point in the first array based on x-values
            for point1 in sorted_array1:
                distance = abs(point2[0] - point1[0])
                if distance < min_distance:
                    min_distance = distance
                    associated_point = point1
            
            # Add the association to the list
            if associated_point:
                associations.append((associated_point, point2))

        # Calculate the distances between associated points
        distances = []
        for association in associations:
            dist = association[1][1] - association[0][1]
            distances.append(dist)
        if distances[0] < 0:
            return "up"
        else:
            return "down"


#importing data from the log files
import os 
import re 
log_file_path= "lab_latency.log"

if os.path.exists(log_file_path):
    print('log file exists.')
else:
    print('Log file not found by the RTL Server.')

pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - INFO - Latency: (\d+\.\d+) seconds"
with open(log_file_path,'r') as file:
    log_data=file.read()
matches= re.findall(pattern,log_data)
for match in matches:
   latency=match
print(match)

#importing the direction log data from log files
dir_log_path = "lab_direction.log"
if os.path.exists(dir_log_path):
    pass
else:
    print('direction log file doesnt found.')
# dir_pattern= pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - INFO - "
# with open(dir_log_path,'r') as file:
#     dir_log_data=file.read()
# dir=re.findall(dir_pattern,dir_log_data)
# for i in dir:
#     tt, state=i


with open(dir_log_path, 'r') as file:
    dir_log_data = file.readlines()

dir_log_ent = dir_log_data[-1].strip() if dir_log_data else None
print(dir_log_ent)

# beaker liquid
# liquid_level_values = list(level.values())
# print("Liquid level of oil and water is approx. : " ,liquid_level_values)
lev=0
for beaker, level in level.items():
    if level < 90:
        lev=1
    else:
        lev=0


l = ["moving_down_lab/","moving_up_lab/"]
direction_check = []

for i in l:
    movement_code = compare_ss(i)
    direction_check.append(movement_code)
    if movement_code == "up":
        #logging.warning('Movement: Upwards\n')
        pass
    elif movement_code == "down":
        #logging.warning('Movement: Downwards\n')
        pass
    elif movement_code == "still":
        logging.warning('Movement: Still\n')

if direction_check[0] == direction_check[1] == "still" or lev==1 :
    recipients = ["nageshwalchtwar257@gmail.com"]
    send_email(recipients, '''Hi, I'm Vanishing Rod,
                                                The experiment is having some issues, the Rods are still or the Video stream not showing during the process or liquid level is LOW. Kindly check the experiment 
                                                    - Maintainance Team ( Vanishing Rod ) ''', 'mail sent')
elif direction_check[0] == "still" and direction_check[1] == "up": 
    recipients = ["nageshwalchtwar257@gmail.com"]
    send_email(recipients, ''' Hi, I'm Vanishing Rod,
                                                Experiment is having some issue,
                                                Recalibation issue is there. 
                                                kindly check the experiment 
                                                    - Maintainance Team ( Vanishing Rod )''', 'mail sent')
elif direction_check[0] == "up" and direction_check[1] == "down":
    recipients = ["nageshwalchtwar257@gmail.com", "vedant.nipane@students.iiit.ac.in","rishabh.agrawal@students.iiit.ac.in","abhinav.marri@research.iiit.ac.in"]
    send_email(recipients, ''' Hi, I'm Vanishing Rod,
                                                Experiment is having some issue, Direction change and threads are wound up.
                                                kindly check the experiment 
                                                    - Maintainance Team ( Vanishing Rod )''', 'mail sent')
elif direction_check[0] == "down" and direction_check[1] == "up" or direction_check[1]=="still":
    recipients = ["theccbussiness@gmail.com"]
    logging.info('Works successfully\n')
    send_email(recipients, '''Hi,I'm Vanishing Rod, experiment working fine. The latency (seconds) is {match}!
                - Maintainance Team ( Vanishing Rod ) '''.format(match=match) , 'mail sent')




print(direction_check)







