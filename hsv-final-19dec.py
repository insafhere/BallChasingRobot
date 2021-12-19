from picamera.array import PiRGBArray     #As there is a resolution problem in raspberry pi, will not be able to capture frames by VideoCapture
from picamera import PiCamera
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

def nothing(x):
    pass

cv2.namedWindow("HSV Trackbar")

cv2.createTrackbar("L - H", "HSV Trackbar", 0, 179, nothing)
cv2.createTrackbar("L - S", "HSV Trackbar", 0, 255, nothing)
cv2.createTrackbar("L - V", "HSV Trackbar", 0, 255, nothing)
cv2.createTrackbar("U - H", "HSV Trackbar", 179, 179, nothing)
cv2.createTrackbar("U - S", "HSV Trackbar", 255, 255, nothing)
cv2.createTrackbar("U - V", "HSV Trackbar", 255, 255, nothing)

def find_blob(blob): #returns the red colored circle
	largest_contour=0
	cont_index=0
	_, contours, _ = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for idx, contour in enumerate(contours):
		area=cv2.contourArea(contour)
		if (area >largest_contour) :
	    		largest_contour=area

	    		cont_index=idx
			#if res>15 and res<18:
			#    cont_index=idx

	r=(0,0,2,2)
	if len(contours) > 0:
		r = cv2.boundingRect(contours[cont_index])

	return r,largest_contour

def target_hist(frame):
	hsv_img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	hist=cv2.calcHist([hsv_img],[0],None,[50],[0,255])
	return hist

#CAMERA CAPTURE
#initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (160, 128)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=(160, 128))
 
# allow the camera to warmup
time.sleep(0.001)
 
# capture frames from the camera
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
	frame = image.array
	frame=cv2.flip(frame,1)
	global centre_x
	global centre_y
	centre_x=0.
	centre_y=0.
	
	l_h = cv2.getTrackbarPos("L - H", "HSV Trackbar")
	l_s = cv2.getTrackbarPos("L - S", "HSV Trackbar")
	l_v = cv2.getTrackbarPos("L - V", "HSV Trackbar")
	u_h = cv2.getTrackbarPos("U - H", "HSV Trackbar")
	u_s = cv2.getTrackbarPos("U - S", "HSV Trackbar")
	u_v = cv2.getTrackbarPos("U - V", "HSV Trackbar")
	
	hsv_lower = np.array([l_h, l_s, l_v])
	hsv_upper = np.array([u_h, u_s, u_v])
	
	cv2.imshow("frame", frame)
	hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask_1 = cv2.inRange(hsv_roi, hsv_lower, hsv_upper)
	cv2.imshow('HSV Mask',mask_1)

	result = cv2.bitwise_and(frame, frame, mask=mask)
	cv2.imshow('result',result)     
	
	loct,area=find_blob(mask_1)
	x,y,w,h=loct
	
	simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
	centre_x=x+((w)/2)
	centre_y=y+((h)/2)
	frame = cv2.circle(frame,(int(centre_x),int(centre_y)),3,(0,110,255),-1)
	centre_x = 80 - centre_x
	centre_y= 64 - centre_y
	print("Centre x is : " , centre_x,"Centre y is : ", centre_y)
    
