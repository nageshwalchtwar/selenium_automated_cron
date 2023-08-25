import cv2
import os
import numpy as np

def get_liquid_levels(image_path):

    rectangles = [
        (45, 252, 316, 463),  # Rectangle for beaker 1 
        (553, 249, 323, 472)  # Rectangle for beaker 2 
    ]

 
    screenshot = cv2.imread(image_path)

    liquid_levels = {}


    for idx, rect in enumerate(rectangles):
        x, y, w, h = rect

        roi = screenshot[y:y+h, x:x+w]

        # Convert the ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_roi, threshold1=30, threshold2=150)

        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=20, maxLineGap=7)

        liquid_level = None
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if y1 > (h // 2) and y2 > (h // 2): 
                    liquid_level = y1  
                    break  
        if liquid_level is not None:
            liquid_level_percentage = ((h - (liquid_level - y)) / h) * 100
            liquid_levels[f"Beaker {idx + 1}"] = liquid_level_percentage

    return liquid_levels


screenshot_path = "moving_down_lab/screenshot_0.png"
liquid_levels = get_liquid_levels(screenshot_path)
print(liquid_levels)
