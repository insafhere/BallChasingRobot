import cv2
import numpy as np 
from picamera.array import PiRGBArray
from picamera import PiCamera 

def nothing(x):
    pass
 
im = np.zeros((300,512,3), np.uint8)
cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	img = frame.array

	# Convert BGR to HSV
	imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	B = cv2.getTrackbarPos("B", "Trackbars")
	G = cv2.getTrackbarPos("G", "Trackbars")
	R = cv2.getTrackbarPos("R", "Trackbars")

	im[:] = [B, G, R]

	green = np.uint8([[[B, G, R]]])
	hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
	lowerBound = np.uint8([hsvGreen[0][0][0]-10,100,100])
	upperBound = np.uint8([hsvGreen[0][0][0]+10,255,255])

	# Create the Mask
	mask=cv2.inRange(imgHSV,lowerBound,upperBound)

	# Morphology
	maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
	maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

	maskFinal=maskClose
	_, conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

	for i in range(len(conts)):
		x,y,w,h=cv2.boundingRect(conts[i])
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)

	cv2.imshow("mask",mask)
	cv2.imshow("cam",img)
	cv2.imshow("Trackbars",im)

	key = cv2.waitKey(1)
	rawCapture.truncate(0)
	if key == 27:
		break

cv2.destroyAllWindows()
