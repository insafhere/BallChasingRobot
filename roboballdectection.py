# OpenCV HSV range is: H: 0 to 179 S: 0 to 255 V: 0 to 255
# To find a color, usually just look up for the range of H and S, and set v in range(20, 255).
# use HSVFinder.py to find lower and upper limit HSV value

import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    
    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    
    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)
    
    # Every color except white
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    exceptwhite = cv2.bitwise_and(frame, frame, mask=mask)
    
    #RoboMaster Balls 
    # OpenCV HSV Range, H (0-179), S (0-255), V (0-255)
    low_robo = np.array([24,39,88])
    high_robo = np.array([66,131,255])
    robo_mask = cv2.inRange(hsv_frame,low_robo,high_robo) # only the robo balls will be white
    robo = cv2.bitwise_and(frame, frame, mask=robo_mask) #only the robo in color will be seen
                      
    cv2.imshow("Frame", frame) #colored picture will be shown
    #cv2.imshow("Red", red)
    #cv2.imshow("Blue", blue)
    #cv2.imshow("Green", green)
    #cv2.imshow("Except White", exceptwhite)
    cv2.imshow("Robo Balls", robo)                   
    key = cv2.waitKey(1)
    if key == 27:
        break
