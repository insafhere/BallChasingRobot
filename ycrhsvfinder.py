import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - Y", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - C", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - R", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - Y", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - C", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - R", "Trackbars", 255, 255, nothing)

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
	frame1 = cv2.flip(frame,-1)
	frame2 = cv2.flip(frame,-1)

	#YCR
	ycr = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

	l_y = cv2.getTrackbarPos("L - Y", "Trackbars")
	l_c = cv2.getTrackbarPos("L - C", "Trackbars")
	l_r = cv2.getTrackbarPos("L - R", "Trackbars")
	u_y = cv2.getTrackbarPos("U - Y", "Trackbars")
	u_c = cv2.getTrackbarPos("U - C", "Trackbars")
	u_r = cv2.getTrackbarPos("U - R", "Trackbars")

	ycr_lower = np.array([l_y, l_c, l_r])
	ycr_upper = np.array([u_y, u_c, u_r])

	ycr_mask = cv2.inRange(ycr, ycr_lower, ycr_upper)
	ycr_result = cv2.bitwise_and(ycr_mask, frame1)

	loct1,area1=find_blob(ycr_mask)
	x1,y1,w1,h1=loct1	
	cv2.rectangle(frame, (x1,y1), (x1+w1,y1+h1), 255,2)
	ycr_centre_x=x1+((w1)/2)
	ycr_centre_y=y1+((h1)/2)
	cv2.circle(frame,(int(ycr_centre_x),int(ycr_centre_y)),3,(0,255,0),-1)
	print("YCR Centre x is : " , ycr_centre_x,"YCR Centre y is : ", ycr_centre_y)

	#HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	l_h = cv2.getTrackbarPos("L - H", "Trackbars")
	l_s = cv2.getTrackbarPos("L - S", "Trackbars")
	l_v = cv2.getTrackbarPos("L - V", "Trackbars")
	u_h= cv2.getTrackbarPos("U - H", "Trackbars")
	u_s= cv2.getTrackbarPos("U - S", "Trackbars")
	u_v= cv2.getTrackbarPos("U - V", "Trackbars")

	hsv_lower = np.array([l_h, l_s, l_v])
	hsv_upper = np.array([u_h, u_s, u_v])

	hsv_mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
	hsv_result = cv2.bitwise_and(hsv_mask_frame2)

	loct2,area2=find_blob(hsv_mask)
	x2,y2,w2,h2=loct2	
	cv2.rectangle(frame, (x2,y2), (x2+w2,y2+h2), 255,2)
	hsv_centre_x=x2+((w2)/2)
	hsv_centre_y=y2+((h2)/2)
	cv2.circle(frame,(int(hsv_centre_x),int(hsv_centre_y)),3,(0,0,255),-1)
	print("HSV Centre x is : " , hsv_centre_x,"HSV Centre y is : ", hsv_centre_y)

	#IMSHOW
	cv2.imshow("frame", frame)

	cv2.imshow("ycr mask", ycr_mask)
	cv2.imshow("ycr result", ycr_result)

	cv2.imshow("hsv mask", hsv_mask)
	cv2.imshow("hsv result", hsv_result)

	key = cv2.waitKey(1)
	if key == 27:
		break
