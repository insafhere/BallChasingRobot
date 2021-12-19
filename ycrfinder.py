import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


def find_blob(blob): #returns the robo green colored circle
      largest_contour=0
      cont_index=0
      _, contours, _ = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      for idx, contour in enumerate(contours):
            area=cv2.contourArea(contour)
            if (area >largest_contour) :
                  largest_contour=area
                  cont_index=idx                   
      r=(0,0,2,2)
      if len(contours) > 0:
            r = cv2.boundingRect(contours[cont_index])
      
      print("r is : " , r, "largest contour is : " , largest_contour)
      return r,largest_contour

while True:
	_, frame = cap.read()
	frame=cv2.flip(frame,-1)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
	
	l_h = cv2.getTrackbarPos("L - H", "Trackbars")
	l_s = cv2.getTrackbarPos("L - S", "Trackbars")
	l_v = cv2.getTrackbarPos("L - V", "Trackbars")
	u_h = cv2.getTrackbarPos("U - H", "Trackbars")
	u_s = cv2.getTrackbarPos("U - S", "Trackbars")
	u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
	lower_blue = np.array([l_h, l_s, l_v])
	upper_blue = np.array([u_h, u_s, u_v])
	
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	result = cv2.bitwise_and(frame, frame, mask=mask)
	
	loct,area=find_blob(mask)
	x,y,w,h=loct
	
	simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
	centre_x=x+((w)/2)
	centre_y=y+((h)/2)
	frame = cv2.circle(frame,(int(centre_x),int(centre_y)),3,(0,110,255),-1)
	centre_x-=80
	centre_y=6--centre_y
	print("Centre x is : " , centre_x,"Centre y is : ", centre_y)

	cv2.imshow("frame", frame)
	cv2.imshow("mask", mask)
	cv2.imshow("result", result)

	key = cv2.waitKey(1)
	if key == 27:
		break
