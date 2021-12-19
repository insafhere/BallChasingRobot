from picamera.array import PiRGBArray     #As there is a resolution problem in raspberry pi, will not be able to capture frames by VideoCapture
from picamera import PiCamera
import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow("HSV Trackbar")
cv2.namedWindow("YCR Trackbar")

cv2.createTrackbar("L - H", "HSV Trackbar", 0, 255, nothing)
cv2.createTrackbar("L - S", "HSV Trackbar", 0, 255, nothing)
cv2.createTrackbar("L - V", "HSV Trackbar", 0, 255, nothing)
cv2.createTrackbar("U - H", "HSV Trackbar", 179, 179, nothing)
cv2.createTrackbar("U - S", "HSV Trackbar", 255, 255, nothing)
cv2.createTrackbar("U - V", "HSV Trackbar", 255, 255, nothing)

cv2.createTrackbar("L - Y", "YCR Trackbar", 0, 255, nothing)
cv2.createTrackbar("L - C", "YCR Trackbar", 0, 255, nothing)
cv2.createTrackbar("L - R", "YCR Trackbar", 0, 255, nothing)
cv2.createTrackbar("U - Y", "YCR Trackbar", 179, 179, nothing)
cv2.createTrackbar("U - C", "YCR Trackbar", 255, 255, nothing)
cv2.createTrackbar("U - R", "YCR Trackbar", 255, 255, nothing)


#Image analysis work
def segment_colour(frame):    #returns only the red colors in the frame
	cv2.imshow("frame", frame)
	hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask_1 = cv2.inRange(hsv_roi, hsv_lower, hsv_upper)
	cv2.imshow('HSV Mask',mask_1)
	
	ycr_roi=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
	mask_2=cv2.inRange(ycr_roi, ycr_lower, ycr_upper)
	cv2.imshow('YCR Mask',mask_2)

	mask = mask_1 | mask_2
	kern_dilate = np.ones((8,8),np.uint8)
	kern_erode  = np.ones((3,3),np.uint8)
	mask= cv2.erode(mask,kern_erode)      #Eroding
	mask=cv2.dilate(mask,kern_dilate)     #Dilating
	cv2.imshow('mask',mask)
	
	result = cv2.bitwise_and(frame, frame, mask=mask)
	cv2.imshow('result',result)
	
	return mask

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
camera.resolution = (160, 120)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=(160, 120))
 
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
	
	l_y = cv2.getTrackbarPos("L - Y", "YCR Trackbar")
	l_c = cv2.getTrackbarPos("L - C", "YCR Trackbar")
	l_r = cv2.getTrackbarPos("L - R", "YCR Trackbar")
	u_y = cv2.getTrackbarPos("U - Y", "YCR Trackbar")
	u_c = cv2.getTrackbarPos("U - C", "YCR Trackbar")
	u_r = cv2.getTrackbarPos("U - R", "YCR Trackbar")
	
	ycr_lower = np.array([l_y, l_c, l_r])
	ycr_upper = np.array([u_y, u_c, u_r])
	
	mask=segment_colour(frame)      #masking after both ycr and hsv
	loct,area=find_blob(mask_red)
	x,y,w,h=loct
	
	
	simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
	centre_x=x+((w)/2)
	centre_y=y+((h)/2)
	frame = cv2.circle(frame,(int(centre_x),int(centre_y)),3,(0,110,255),-1)
	centre_x = 80 - centre_x
	centre_y= 60 - centre_y
	print("Centre x is : " , centre_x,"Centre y is : ", centre_y)

	cv2.imshow("frame", frame)
	
	cv2.imshow("mask", mask)
	cv2.imshow("result", result)
     
	#cv2.imshow("draw",frame)    
	rawCapture.truncate(0)  # clear the stream in preparation for the next frame
