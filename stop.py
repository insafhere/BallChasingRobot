# import the necessary packages
from picamera.array import PiRGBArray     #As there is a resolution problem in raspberry pi, will not be able to capture frames by VideoCapture
from picamera import PiCamera
import RPi.GPIO as GPIO
import time

import numpy as np

#hardware work
GPIO.setmode(GPIO.BCM)


#OUT3 to GPIO25
#OUT4 to GPIO8
MOTOR1B=25  #Left Motor
MOTOR1E=8

#OUT1 to GPIO23
#OUT2 to GPIO15
MOTOR2B=23  #Right Motor
MOTOR2E=15

LED_PIN=13  #If it finds the ball, then it will light up the led


GPIO.setup(LED_PIN,GPIO.OUT)

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
     
def leftturn():
      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR1E,GPIO.HIGH)
      GPIO.output(MOTOR2B,GPIO.HIGH)
      GPIO.output(MOTOR2E,GPIO.LOW)
     
def rightturn():
      GPIO.output(MOTOR1B,GPIO.HIGH)
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.HIGH)

def stop():
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)

print("Stop")
stop()
