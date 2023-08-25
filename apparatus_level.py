import cv2
import os
import numpy as np

def get_liquid_levels(image_path):
    # Manually define the rectangles for the two beakers
    rectangles = [
        (45, 252, 316, 463),  # Rectangle for beaker 1 (x, y, width, height)
        (553, 249, 323, 472)  # Rectangle for beaker 2 (x, y, width, height)
    ]

    # Load the screenshot image
    screenshot = cv2.imread(image_path)

    liquid_levels = {}

    # Process the rectangles and calculate liquid levels
    for idx, rect in enumerate(rectangles):
        x, y, w, h = rect

        # Extract the region of interest (ROI) within the rectangle
        roi = screenshot[y:y+h, x:x+w]

        # Convert the ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply edge detection to the grayscale ROI
        edges = cv2.Canny(gray_roi, threshold1=30, threshold2=150)

        # Find the horizontal lines in the edge-detected ROI
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=20, maxLineGap=7)
        
        # Calculate the liquid level based on the detected lines
        liquid_level = None
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if y1 > (h // 2) and y2 > (h // 2):  # Consider only lines below the middle
                    liquid_level = y1  # Use y1 coordinate as liquid level
                    break  # Take the first detected line as the liquid level

        if liquid_level is not None:
            liquid_level_percentage = ((h - (liquid_level - y)) / h) * 100
            liquid_levels[f"Beaker {idx + 1}"] = liquid_level_percentage

    return liquid_levels

# Example usage
screenshot_path = "moving_down_lab/screenshot_0.png"
liquid_levels = get_liquid_levels(screenshot_path)
print(liquid_levels)
