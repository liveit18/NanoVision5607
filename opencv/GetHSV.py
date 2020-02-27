#!/usr/bin/env python3
import cv2
import numpy
import glob
from goalpipeline import *

def onmouse(k,x,y,s,p):
    global hsv
    if k==1:   # left mouse, print pixel at x,y
        print(hsv[y,x])
cap = cv2.VideoCapture('test.mov')
goal = GoalPipeline()
while cap.isOpened():
    ret, rawImage = cap.read()
#for imageFile in glob.glob('./*.jpg'):
#    rawImage = cv2.imread(imageFile)
    goal.process(rawImage)
    cv2.imshow('Original Image',rawImage)
    cv2.moveWindow('Original Image', 40,30) 
    cv2.imshow("Blur", goal.blur_output)
    cv2.moveWindow('Blur', 480,30) 
    cv2.imshow('erode',goal.cv_erode_0_output)
    cv2.moveWindow('erode', 40,480) 
    cv2.imshow('dilate',goal.cv_dilate_0_output)
    cv2.moveWindow('dilate', 480,480) 
    cv2.imshow('Final',goal.cv_erode_1_output)
    cv2.moveWindow('Final', 960,480) 

    #hsv = cv2.cvtColor(rawImage, cv2.COLOR_BGR2HLS)
    #red =   [80, 165]
    #green = [240, 254]
    #blue =  [250, 255]
    #cv2.namedWindow("hsv")
    #cv2.setMouseCallback("hsv",onmouse);
    #cv2.imshow('hsv',hsv)
    #mask = cv2.inRange(hsv, (red[0], green[0], blue[0]),  (red[1], green[1], blue[1]))
    #cv2.inRange(hsv, lower_green, upper_green)
    #res = cv2.bitwise_and(rawImage,rawImage,mask=mask)
    #cv2.imshow('MASK',res)
    if cv2.waitKey() & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
    
# HSV   
#[ 70   3 255]  
#[ 45   2 255]  
#[  0   0 255]  
#[  0   0 255]  
#[ 30   2 255]  
#[ 38   4 255]  
#[ 25   6 254]  
#[ 90   1 255]  
#[150   1 255]  
#[ 90   4 255]  
#[ 75   4 255]  
#[ 45   2 255]  
#[ 84   5 255]  
#[ 90   1 255]  
#[ 96   5 255]  
#[ 90   3 255]  
#[ 90   9 255]  
#[ 30   2 255]  
#[ 90  12 255]  
#[ 30   2 255]  
#[150   1 255]  
#[  0   0 255]  
#[ 90  12 255]  
#[ 90  13 255]  
#[ 75   4 255]  
#[ 30   2 252]  
#[ 89  49 255]  
#[ 90  48 255]  
#[ 90   6 255]  
#[ 90   7 255]  
#[  0   0 255]  
#[150   3 255]  
#[135   2 255]  
#[ 90   4 255]  
#[ 90   4 255]  
#[150   1 255]  
#[  0   0 255]  
#[150   1 255]  
#[ 90   3 255]  
#[100   6 255]  
#[ 90  10 255]  
#[150   2 255]  
#[ 90  15 255]  
#[ 90   5 255]  
#[ 90   8 255]  
#[ 15   2 255]  
#[  0   0 255]  
#[ 83   4 254]  
#[ 80   9 253]  
#[ 30   2 255]  
#[  0   0 255]  
#[ 90   5 255]  
#[135   2 255]  
#[150   4 255]  
#[150   1 255]  
#[ 30   4 255]  
#[ 90   7 255]  
#[105   2 255]  
#[ 90  15 255]  
#[ 90   4 255]  
#[ 75   4 255]  
#[150   1 255]  
#[135   2 255]  
#[150   1 255]  
#[ 90   8 255]  
#[ 45   2 255]  
#[ 75   2 252]  
#[165   2 254]  
#[ 90   1 255]  
#[ 90   5 255]  
#[ 90   1 255]  
#[150   1 255]  
#[  0   0 255]  
#[ 90   1 255]  
#[ 60   6 255]  
#[ 90   1 255]  
#[ 45   2 255]  
#[ 90   4 255]  
#[ 40   9 255]  
#[  0   0 255]  
#[ 50   3 250]  
#[150   4 255]  
#[ 90   1 255]  
#[ 45   2 255]  
#[150   1 255]  
#[150   1 255]  
#[120   1 255]  
#[150   1 255]  
#[ 90   1 255]  
#[ 90   3 255]  

# HLS
#[ 90 251 255]
#[ 37 253 255]
#[ 90 247 255]
#[ 90 251 255]
#[105 254 255]
#[ 90 254 255]
#[ 69 252 255]
#[ 30 254 255]
#[ 90 254 255]
#[ 60 252 255]
#[ 97 253 255]
#[ 90 254 255]
#[ 90 247 255]
#[ 90 253 255]
#[ 90 245 255]
#[  0 255   0]
#[150 254 255]
#[ 90 253 255]
#[150 254 255]
#[ 90 251 255]
#[150 254 255]
#[ 90 254 255]
#[ 37 253 255]
#[ 90 252 255]
#[ 90 254 255]
#[138 253 255]
#[ 90 251 255]
#[ 90 232 255]
#[ 90 238 255]
#[ 90 249 255]
#[ 90 254 255]
#[ 90 254 255]
#[120 254 255]
#[ 90 253 255]
#[150 254 255]
#[ 90 254 255]
#[120 254 255]
#[ 90 250 255]
#[150 254 255]
#[ 83 251 255]
#[ 90 254 255]
#[ 90 252 255]
#[ 83 246 255]
#[ 83 253 255]
#[ 90 251 255]
#[ 90 250 255]
#[ 90 246 255]
#[126 252 182]
#[120 254 255]
#[ 90 254 255]
#[150 253 255]
#[ 90 251 255]
#[140 251  85]
#[ 90 254 255]
#[ 90 254 255]
#[ 90 253 255]
#[130 254 255]
#[150 254 255]
#[ 90 254 255]
#[102 253 255]
#[ 75 253 255]
#[ 30 254 255]
#[ 90 253 255]
#[ 90 253 255]
#[ 90 249 255]
#[ 90 253 255]
#[120 254 255]
#[150 254 255]
#[ 90 252 255]
#[150 254 255]
#[165 254 255]
#[ 90 252 255]
#[  6 251 142]
#[150 254 255]
#[ 50 254 255]
#[150 253 255]
#[ 90 254 255]
#[ 80 251 255]
#[ 90 251 255]
#[ 90 254 255]
#[ 90 254 255]
#[120 253 255]
#[ 90 252 255]
#[ 90 254 255]