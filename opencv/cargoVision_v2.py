#!/usr/bin/env python3
#
# Demonstrates streaming and modifying the image via OpenCV
#    hue = [12, 95]
 #   sat = [100, 255]
  #  val = [32, 255]


import cscore as cs
import numpy as np
import cv2
#from powercellcv import *
from networktables import NetworkTables
def preprocess(frame):

    out = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    out = cv2.blur(out,(blur_ksize, blur_ksize))
    out = cv2.inRange(out, (hue_red[0], sat_red[0], val_red[0]),  (hue_red[1], sat_red[1], val_red[1]))
    out = cv2.inRange(out, (hue_blue[0], sat_blue[0], val_blue[0]),  (hue_blue[1], sat_blue[1], val_blue[1]))
    return out

def cargoProcess(frame, color, label, sd):

    out = cv2.dilate(out, kernel, anchor, iterations = 3)#, cv2.BORDER_CONSTANT , bordervalue)########
    out = cv2.erode(out, kernel, anchor, iterations = 2)#, cv2.BORDER_CONSTANT , bordervalue)
    cnts, a = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    center = None

    #only do stuff if a single contor was found
    if len(cnts) > 0:
        #find the largest contour in the mask, then use it
        #to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        ## v wouldn't run after the return?
        try:
            center = (int(M["m10"] / M["m00"]), int (M["m01"] / M["m00"]))
            data = [center, radius]
            return data

        except ZeroDivisionError:
            center = [0,0]
            data = center, radius
            return data

def drawCircle(frame, center, radius, color,label, minRadius = 7):
    '''
    frame = image
    center = (x,y)
    radius = int
    color = (R,G,B)

    '''
    if radius > minRadius:
                    #draw a circle around the target and publish values to smart dashboard
        cv2.circle(frame, center, int(radius), color, 2)### change here color is a R

        #MDH EXample label is text like red or blue that is
        # # sd.putNumber(f'X_{label}',x)## add a s
        #print("X: " + repr(round(x, 1)) + " Y: " + repr(round(y, 1)) + " Radius: " + repr(round(radius, 1)
        sd.putNumber(f'X_{label}',x)  ## tuple
        sd.putNumber(f'Y_{label}', y) #tuple
        sd.putNumber(f'R_{label}',radius)
    else:
        sd.putNumber(f'X_{label}', 0)  ## tuple
        sd.putNumber(f'Y_{label}', 0) #tuple
        sd.putNumber(f'R_{label}', 0)

    return frame



def main():
    SCALE=2
    WIDTH=160*SCALE
    HEIGHT=90*SCALE
    FPS=15
    hue_red = [0, 180]
    sat_red = [137, 223.0]
    val_red = [127, 255.0]


    hue_blue = [92, 115]
    sat_blue = [126, 235]
    val_blue = [36, 183]
    #blur_type = BlurType.Box_Blur
    blur_radius = 10
    blur_ksize = int(2 * round(blur_radius) + 1)
    #powercell = powercellcv()
    camera = cs.UsbCamera("usbcam", 0)
    camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

   # mjpegServer = cs.MjpegServer("httpserver", 8081)
   # mjpegServer.setSource(camera)

   # print("mjpg server listening at http://0.0.0.0:8081")

    cvsink = cs.CvSink("cvsink")
    cvsink.setSource(camera)

    cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)
    cvMjpegServer = cs.MjpegServer("Goal", 8082)
    cvMjpegServer.setSource(cvSource)

    print("OpenCV output mjpg server listening at http://0.0.0.0:8082")

    test = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    flip = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    #out = self.hsv_threshold_output
    kernel = None
    anchor = (-1, -1)
    iterations = 1.0
    bordertype = cv2.BORDER_CONSTANT
    bordervalue = (-1)

    #=====
    NetworkTables.initialize(server='roborio-5607-frc.local')
    sd = NetworkTables.getTable("cargo")
  # cs2 = cs2.getInstance()
  # cs2.enableLogging()

  # camera2 = cs2.startAutomaticCapture()

  # camera2.setResolution(320, 240)

  # # Get a CvSink. This will capture images from the camera
  # cvSink2 = cs2.getVideo()

  # # (optional) Setup a CvSource. This will send images back to the Dashboard
  # outputStream2 = cs2.putVideo("Rectangle", 320, 240)

  # # Allocating new images is very expensive, always try to preallocate
  # img2 = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

  # while True:
  #     # Tell the CvSink to grab a frame from the camera and put it
  #     # in the source image.  If there is an error notify the output.
  #     time, img = cvSink.grabFrame(img)


    while True:

        time, frame = cvsink.grabFrame(test)
        if time == 0:
            print("error:", cvsink.getError())
            continue

        #print("got frame at time", time, test.shape)

        #cv2.flip(test, flipCode=0, dst=flip)

        ### preprossesing
        ## have out blue and out red, repeat in a func that passes vals
        '''
        '''
        labels = ["blue","red"]
        out = preprocess(frame)

        for label in labels:
            if label == "red":
                color = (255,0,0)
            else:
                color = (0,0,255)
            centers, rad = cargoProcess(out , color, label, sd)

            out = drawCircle(out, centers, rad, color,label, minRadius = 7)
###
###
        '''def colors(frame, color, label, sd):

            out = cv2.dilate(out, kernel, anchor, iterations = 3)#, cv2.BORDER_CONSTANT , bordervalue)########
            out = cv2.erode(out, kernel, anchor, iterations = 2)#, cv2.BORDER_CONSTANT , bordervalue)
            cnts, a = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            center = None

            #only do stuff if a single contor was found
            if len(cnts) > 0:
                #find the largest contour in the mask, then use it
                #to compute the minimum enclosing circle and centroid
                c = max(cnts, key=cv2.contourArea)
                ((x,y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                return [x,y,radius]
                try:
                    center = (int(M["m10"] / M["m00"]), int (M["m01"] / M["m00"]))
                except ZeroDivisionError:
                    center = (0,0)



                #if the dectected contour has a radius big enough, we will send it
                if radius > 7:
                    #draw a circle around the target and publish values to smart dashboard
                    cv2.circle(frame, center, int(radius), (225,0,0), 2)### change here color is a RGB

                    cv2.circle(frame, center, int(radius), (0,0,225), -1)
                    #MDH EXample label is text like red or blue that is
                    # # sd.putNumber(f'X_{label}',x)## add a s
                    #print("X: " + repr(round(x, 1)) + " Y: " + repr(round(y, 1)) + " Radius: " + repr(round(radius, 1)))

                    sd.putNumber(f'X_{label}',x)  ## add a s
                    sd.putNumber(f'Y_{label}', y)
                    sd.putNumber(f'X_{label}',radius)


                else:
                    #print("WTF")
                    #let the RoboRio Know no target has been detected with -1
                    sd.putNumber(f'X_{label}', x)  ## add a s
                    sd.putNumber(f'Y_{label}', y)
                    sd.putNumber(f'X_{label}', radius)

                return '''
                '''
                '''
#####
        #powercell.process(test)

        cvSource.putFrame(out)



if __name__ == "__main__":
    main()


