# import the necessary packages
from picamera.array import PiRGBArray     #As there is a resolution problem in raspberry pi, will not be able to capture frames by VideoCapture
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import cv2

import numpy as np

#hardware work
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER1 = 27      #Left ultrasonic sensor
GPIO_ECHO1 = 22

GPIO_TRIGGER2 = 19      #Front ultrasonic sensor
GPIO_ECHO2 = 26

GPIO_TRIGGER3 = 5      #Right ultrasonic sensor
GPIO_ECHO3 = 6

MOTOR1B=25  #Left Motor
MOTOR1E=8

MOTOR2B=23  #Right Motor
MOTOR2E=15
en = 24
en1 = 14
LED_PIN=13  #If it finds the ball, then it will light up the led

# Set pins as output and input

GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO1,GPIO.IN)   

GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO2,GPIO.IN)

GPIO.setup(GPIO_TRIGGER3,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO3,GPIO.IN)

GPIO.setup(LED_PIN,GPIO.OUT)

GPIO.setup(en ,GPIO.OUT)
GPIO.setup(en1 ,GPIO.OUT)

p=GPIO.PWM(en,1000)
p1=GPIO.PWM(en1,1000)

p.start(100)
p1.start(100)

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER1, False)
GPIO.output(GPIO_TRIGGER2, False)
GPIO.output(GPIO_TRIGGER3, False)

# Allow module to settle
def sonar(GPIO_TRIGGER,GPIO_ECHO):
      start=0
      stop=0
      # Set pins as output and input
      GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
      GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
     
      # Set trigger to False (Low)
      GPIO.output(GPIO_TRIGGER, False)
     
      # Allow module to settle
      time.sleep(0.01)
           
      #while distance > 5:
      #Send 10us pulse to trigger
      GPIO.output(GPIO_TRIGGER, True)
      time.sleep(0.00001)
      GPIO.output(GPIO_TRIGGER, False)
      begin = time.time()
      while GPIO.input(GPIO_ECHO)==0 and time.time()<begin+0.05:
            start = time.time()
     
      while GPIO.input(GPIO_ECHO)==1 and time.time()<begin+0.1:
            stop = time.time()
     
      # Calculate pulse length
      elapsed = stop-start
      # Distance pulse travelled in that time is time
      # multiplied by the speed of sound (cm/s)
      distance = elapsed * 34000
     
      # That was the distance there and back so halve the value
      distance = distance / 2
    
      # Reset GPIO settings
      return distance


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
    mask_1 = cv2.inRange(hsv_roi, np.array([31, 35,133]), np.array([53,177,182]))
    ycr_roi=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
    mask_2=cv2.inRange(ycr_roi, np.array([135, 109, 37]), np.array([166,129,120]))

    mask = mask_1 | mask_2
    kern_dilate = np.ones((8,8),np.uint8)
    kern_erode  = np.ones((3,3),np.uint8)
    mask= cv2.erode(mask,kern_erode)      #Eroding
    mask=cv2.dilate(mask,kern_dilate)     #Dilating
    cv2.imshow('mask',mask)
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

def sensormeasure():
      C = sonar(GPIO_TRIGGER2,GPIO_ECHO2)
      L = sonar(GPIO_TRIGGER1,GPIO_ECHO1)
      R = sonar(GPIO_TRIGGER3,GPIO_ECHO3)
     
def centresensor():
      sonar(GPIO_TRIGGER2,GPIO_ECHO2)
def rightsensor():
      sonar(GPIO_TRIGGER3,GPIO_ECHO3)
def leftsensor():
      sonar(GPIO_TRIGGER1,GPIO_ECHO1)


# capture frames from the camera
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      #grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
      frame = image.array
      frame=cv2.flip(frame,-1)
      global centre_x
      global centre_y
      centre_x=0.
      centre_y=0.
      hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      mask_red=segment_colour(frame)      #masking red the frame
      loct,area=find_blob(mask_red)
      x,y,w,h=loct

      #distance coming from front ultrasonic sensor     
      #distanceC = sonar(GPIO_TRIGGER2,GPIO_ECHO2)
      #print("Distance Centre : %.1f" % distanceC)
      #distance coming from right ultrasonic sensor
      #distanceR = sonar(GPIO_TRIGGER3,GPIO_ECHO3)
      #print("Distance Right: %.1f" % distanceR)
      #distance coming from left ultrasonic sensor
      #distanceL = sonar(GPIO_TRIGGER1,GPIO_ECHO1)
      #print("Distance Left: %.1f" % distanceL)
      
      GPIO.output(LED_PIN,GPIO.LOW)     
      
      #wxh_Area = w*h
      
      #print("w x h: %.1f" % wxh_Area)
      #print("Area: %.1f" % area)
      
      #if (wxh_Area) < 10:
            #found=0
      #else:
            #found=1
            #simg2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
            #centre_x=x+((w)/2)
            #centre_y=y+((h)/2)
            #cv2.circle(frame,(int(centre_x),int(centre_y)),3,(0,110,255),-1)
            #centre_x = 80 - centre_x
            #centre_y= 60 - centre_y
            #print(centre_x,centre_y)
            #GPIO.output(LED_PIN,GPIO.HIGH)
      #initial=80
      
      sensormeasure():

      if(L<25 and C<25 and R<25):
            rightturn()
            time.sleep(3)
      if(L>25 and C<25 and R<25):
            leftturn()
      if(L<25 and C<25 and R>25):
            rightturn()
      if(L>25 and C<25 and R>25):
            rightturn()
      if(L<25 and C>25 and R>25):
            rightturn() 
            time.sleep(180)
            forward()
      if(L>25 and C>25 and R<25):
            leftturn() 
            time.sleep(180)
            forward()
      if(L>25 and C>25 and R>25):
            forward()
            
      #print(direction)
      cv2.imshow("draw",frame)    
      rawCapture.truncate(0)  # clear the stream in preparation for the next frame
         
      if(cv2.waitKey(1) & 0xff == ord('q')):
            break

GPIO.cleanup() #free all the GPIO pins


      

