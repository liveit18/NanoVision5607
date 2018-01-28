import cv2
import numpy as np
from networktables import NetworkTables

import cscore as cs

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

# See https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
gamma = 0.4                                   # change the value here to get different result


#vid = cv2.VideoCapture(0)
##camera server?
SCALE=2
WIDTH=160*SCALE
HEIGHT=90*SCALE
FPS=15
#greenish
hue = [61.01694915254237, 87.44680851063829]
sat = [84.03954802259886, 255.0]
lum = [84.03954802259886, 223.35106382978722]

test = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)

camera = cs.UsbCamera("usbcam", 0)#1, devcam or vid
camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS)

cvsink = cs.CvSink("cvsink")
cvsink.setSource(camera)

cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, WIDTH, HEIGHT, FPS) #get rid of red by nanovision code

cvMjpegServer = cs.MjpegServer("PowerCell", 8081)#here
cvMjpegServer.setSource(cvSource)
count = 0
#NetworkTables.initialize(server='roborio-5607-frc.local')
NetworkTables.initialize(server='192.168.1.135')
# This doesn't work # NetworkTables.initialize(server='DESKTOP-QJOB25H')
sd = NetworkTables.getTable("hub")
sd.putNumber("Test", 1)

while True:
    #count += 1
    time, imageorg = cvsink.grabFrame(test)
    if time == 0:
        print("error:", cvsink.getError())
        continue
    adjusted = adjust_gamma(imageorg, gamma=gamma)
    #image = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HLS)
    image = cv2.cvtColor(imageorg, cv2.COLOR_BGR2HLS)
    image = cv2.inRange(image, (hue[0], lum[0], sat[0]),  (hue[1], lum[1], sat[1]))#dilate, then mask somehow,
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(image, kernel, iterations = (int) (15 +0.5))

    image = cv2.bitwise_and(image, image, mask=mask)
    #cv2.imwrite('source.jpg', image)
    

    # read the image
    #image = cv2.imread('goal.png')

    # convert the image to grayscale format
    #img_gray = cv2.cvtColor(image, cv2.COLOR_BRG2GRAY) #######later
    # apply binary thresholding
    #ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    # visualize the binary image
    #cv2.imshow('Binary image', thresh)
    #cv2.waitKey(0)
    #cv2.imwrite('image_thres1.jpg', thresh)
    #cv2.destroyAllWindows()
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    # draw contours on the original image + dilate the image
    image_copy = imageorg.copy()
    kernel = np.ones((5,5), np.uint8)
    #cv2.dilate(image_copy, kernel, iterations = (int) (15 +0.5))
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    # see the results
    #cv2.imshow('None approximation', image_copy)
    #cv2.waitKey(0)
    #cv2.imwrite('contours_none_image1.jpg', image_copy)
    #cv2.destroyAllWindows()
    ####
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    try:
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x,y,w,h = cv2.boundingRect(biggest_contour)
        image_copy = cv2.rectangle(image_copy, (x,y),(x+w,y+h), color=(0, 255, 0))
    except ValueError:
        x = y = w = h = 0


    sd.putNumber("x_min", x)
    sd.putNumber("x_max", x+w)
    sd.putNumber("y_min", y)
    sd.putNumber("y_max", y+h)
    ##for i in contours: ##had i++, go back through
    ##
    ##    ## Find the area of contour
    ##    a = cv2.contourArea(i,False)
    ##    largest_area = 0
    ##    if(a>largest_area):
    ##        largest_area = a
    ##        print(f'a:{a} and largest_area{largest_area}')
    ##        #cout<<i<<" area  "<<a<<endl;#????does it change
    ##    ## Store the index of largest contour
    ##        largest_contour_index = i
    ##    ##Find the bounding rectangle for biggest contour
    ##        bounding_rect = cv2.boundingRect(contours[i])

    
    #color = cv2.color( 255,255,255)  ##color of the contour in the
    ##  Draw the contour and rectangle
    #cv2.drawContours(image_copy, contours,largest_contour_index, color, cv2.CV_FILLED,8, cv2.hierarchy)
    #cv2.rectangle(image_copy, bounding_rect,  Scalar(0,255,0),2, 8,0)
    #x,y,w,h = cv2.boundingRect(cnt)
    #cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    
    #cv2.namedWindow( "Display window", CV_WINDOW_AUTOSIZE )
    #cv2.imshow( "Display window", src )

    #cv2.imwrite(f'contours_none_image{count}.jpg', image_copy) ##goal vision to push to camserver
    #cv2.waitKey(0)
    #cvSource.putFrame(adjusted)
    cvSource.putFrame(image_copy)

    ###