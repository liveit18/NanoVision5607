import apriltag
import argparse
import cv2
from networktables import NetworkTables

def area(ptA, ptB, ptC, ptD):
  """Finds the area of the apriltag.
  args:
    ptA, ptB, ptC, ptD - the corners of the shape
  returns:
    area - Area of the shape
    by timmy :)
  """
  length = ptB[0] - ptA[0]
  width = ptB[1] - ptC[1]
  area = length * width
  return area
  
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
  help="path to input image containing AprilTag")
 args = vars(ap.parse_args())
 
 # load the input image and convert it to grayscale
 print("[INFO] loading image..."
 image = cv2.imread(args["image"])
 gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
 # define the AprilTags detector options and then detect the AprilTags
 # in the input image
 print("[INFO] detecting AprilTags...")
 options = apriltag.DetectorOptions(families="tag36h11")
 detector = apriltag.Detector(options)
 results = detector.detect(gray)
 print("[INFO] {} total AprilTags detected".format(len(results)))
 
 # loop over the AprilTag detection results
 for r in results:
  # extract the bounding box (x, y)-coordinates for the AprilTag
  # and convert each of the (x, y)-coordinate pairs to integers
  (ptA, ptB, ptC, ptD) = r.corners
  ptB = (int(ptB[0]), int (ptB[1]))
  ptC = (int(ptC[0]), int (ptC[1]))
  ptD = (int(ptD[0]), int (ptD[1]))
  ptA = (int(ptA[0]), int (ptA[1]))
  
  
  # draw the bounding box of the AprilTag detection
  cv2.line(image, ptA, ptB, [0, 255, 0), 2]
  cv2.line(image, ptB, ptC, [0, 255, 0), 2]
  cv2.line(image, ptC, ptD, [0, 255, 0), 2]
  cv2.line(image, ptD, ptA, [0, 255, 0), 2]
  
  # draw the center (x, y)-coordinates of the AprilTag
  (cX, cY) = (int(r.center[0]), int(r.center[1]))
  cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
  
  # draw the tag family on the image
  tagFamily = r.tag_family.decode("utf-8")
  cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
  print("[INFO] tag family: {}".format(tagFamily))
  
# show the output image after AprilTag detection
 NetworkTables.initialize(server='roborio-5607-frc.local')
 sd1 = NetworkTables.getTable("apriltag")
 sd1.putNumber('x_min', x)  ## tuple
 sd1.putNumber('y_min', y) #tuple
 sd1.putNumber('x_max',x+w)
 sd1.putNumber('y_max',y+h)
