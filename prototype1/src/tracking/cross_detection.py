# USAGE
# image file
# python(3) cross_detection.py --image blueCamera.jpg
# take pic with webcam:
# python(3) cross_detection.py 

# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
import time
from imutils.video import VideoStream

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

# if no image is given take a pic with webcam
if not args.get("image",False):
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    image = vs.read()
    vs.stop()
    cv2.destroyAllWindows()
else:
    # load the image
    image = cv2.imread(args["image"])

# find all the 'blue' shapes in the image
lower = np.array([100, 100, 20])
upper = np.array([125, 255, 255])
 # resize and blurring of the image
image = imutils.resize(image, width=600)
blurred = cv2.GaussianBlur(image,(11,11),0)
#convert to hsv color space
hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
# find mask and perform erosion and dilation to remove small blobs in the mask
shapeMask = cv2.inRange(hsv, lower, upper)
shapeMask = cv2.erode(shapeMask, None,iterations=2)
shapeMask = cv2.dilate(shapeMask,None,iterations=2)

# find the contours in the mask and initialize center (x,y) of the ball
cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
center = None

#continue only if there are contours found
if len(cnts) > 0:

    # loop over the contours
    for c in cnts:
        # find radius
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        #find center only if radius is big enough
        if radius > 10:
            # draw the contour and show it
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            # find center
            M= cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 0.0000001
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # draw center and print it only if radius is bigger than certain size
            cv2.circle(image,center, 5 , (0,0,255), -1)
            print("Center : {}".format(center))
            print("radius: {}".format(radius))
        
while True:
    cv2.imshow("Image", image)
    key= cv2.waitKey(1) & 0xFF

    # if q is pressed, get out
    if key == ord("q"):
        break
# close windows
cv2.destroyAllWindows()

 