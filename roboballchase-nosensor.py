#Learn more about HSV, YCR here - https://learnopencv.com/color-spaces-in-opencv-cpp-python/
#Learn more about eroding and dilating - https://docs.opencv.org/3.4.15/db/df6/tutorial_erosion_dilatation.html

# import the necessary packages
from picamera.array import PiRGBArray     #As there is a resolution problem in raspberry pi, will not be able to capture frames by VideoCapture
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import cv2

import numpy as np

#hardware work
GPIO.setmode(GPIO.BCM) #GPIO Numbering

#OUT3 to GPIO25
#OUT4 to GPIO8
MOTOR1B=25  #Left Motor
MOTOR1E=8

#OUT1 to GPIO23
#OUT2 to GPIO15
MOTOR2B=23  #Right Motor
MOTOR2E=15

en = 24
en1 = 14

LED_PIN=13  #If it finds the ball, then it will light up the led

# Set pins as output and input
GPIO.setup(LED_PIN,GPIO.OUT)
GPIO.setup(en ,GPIO.OUT)
GPIO.setup(en1 ,GPIO.OUT)
p=GPIO.PWM(en,1000)
p1=GPIO.PWM(en1,1000)
p.start(100)
p1.start(100)

GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR1E, GPIO.OUT)

GPIO.setup(MOTOR2B, GPIO.OUT)
GPIO.setup(MOTOR2E, GPIO.OUT)

def forward():
      GPIO.output(MOTOR1B, GPIO.HIGH)
      GPIO.output(MOTOR1E, GPIO.LOW)
      GPIO.output(MOTOR2B, GPIO.HIGH)
      GPIO.output(MOTOR2E, GPIO.LOW)
     
def reverse():
      GPIO.output(MOTOR1B, GPIO.LOW)
      GPIO.output(MOTOR1E, GPIO.HIGH)
      GPIO.output(MOTOR2B, GPIO.LOW)
      GPIO.output(MOTOR2E, GPIO.HIGH)
     
def rightturn():
      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR1E,GPIO.HIGH)
      GPIO.output(MOTOR2B,GPIO.HIGH)
      GPIO.output(MOTOR2E,GPIO.LOW)
     
def leftturn():
      GPIO.output(MOTOR1B,GPIO.HIGH)
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.HIGH)

def stop():
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)
     
#Image analysis work
def segment_colour(frame):    #returns only the red colors in the frame
      hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      mask_1 = cv2.inRange(hsv_roi, np.array([45,47,169]), np.array([90,255,255]))
      #ycr_roi=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
      #mask_2=cv2.inRange(ycr_roi, np.array((0.,165.,0.)), np.array((255.,255.,255.)))

      #mask = mask_1 | mask_2
      kern_dilate = np.ones((8,8),np.uint8)
      kern_erode  = np.ones((3,3),np.uint8)
      mask_1= cv2.erode(mask_1,kern_erode)      #Eroding
      mask_1=cv2.dilate(mask_1,kern_dilate)     #Dilating

      #cv2.imshow('mask',mask)
      cv2.imshow('mask1',mask_1)
      #cv2.imshow('mask2',mask_2)
      return mask_1

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

def target_hist(frame):
    hsv_img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    hist=cv2.calcHist([hsv_img],[0],None,[50],[0,255])
    return hist

#CAMERA CAPTURE
#initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.001)
 
# capture frames from the camera
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      #grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
      frame = image.array
      frame=cv2.flip(frame,-1)
      cv2.imshow("frame", frame)
      global centre_x
      global centre_y
      centre_x=0.
      centre_y=0.
      hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      mask_roboball=segment_colour(frame)      #masking red the frame
      loct,area=find_blob(mask_roboball)
      x,y,w,h=loct
             
      if (w*h) < 10:
            found=0
            print("nothingfound")
      else:
            found=1
            print("Found robo ball!")
            simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
            centre_x=x+((w)/2)
            centre_y=y+((h)/2)
            frame = cv2.circle(frame,(int(centre_x),int(centre_y)),3,(0,110,255),-1)
            centre_x-=80
            centre_y=6--centre_y
            print("Centre x is : " , centre_x,"Centre y is : ", centre_y)
      initial=400
      flag=0
      GPIO.output(LED_PIN,GPIO.LOW)          
      if(found==0):
            #if the ball is not found and the last time it sees ball in which direction, it will start to rotate in that direction
            if flag==0:
                  rightturn()
                  time.sleep(0.05)
            else:
                  leftturn()
                  time.sleep(0.05)
            stop()
            time.sleep(0.0125)
     
      elif(found==1):
            if(area<initial):
                forward()
                time.sleep(0.00625)
            elif(area>=initial):
                initial2=6700
                if(area<initial2):
                        #it brings coordinates of ball to center of camera's imaginary axis.
                        if(centre_x<=-20 or centre_x>=20):
                            if(centre_x<0):
                                  flag=0
                                  rightturn()
                                  time.sleep(0.025)
                            elif(centre_x>0):
                                  flag=1
                                  leftturn()
                                  time.sleep(0.025)
                        forward()
                        time.sleep(0.00003125)
                        stop()
                        time.sleep(0.00625)
                else:
                        #if it founds the ball and it is too close it lights up the led.
                        GPIO.output(LED_PIN,GPIO.HIGH)
                        time.sleep(0.1)
                        stop()
                        time.sleep(0.1)
      #cv2.imshow("draw",frame)    
      rawCapture.truncate(0)  # clear the stream in preparation for the next frame
         
      if(cv2.waitKey(1) & 0xff == ord('q')):
            break

GPIO.cleanup() #free all the GPIO pins
