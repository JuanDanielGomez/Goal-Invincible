
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import cv2
import imutils
import time


class Tracker():

    def __init__(self, lowerColorGreen=(25, 80, 15),
                 upperColorGreen=(80, 255, 255),
                 lowerColorBlue=(100, 100, 20),
                 upperColorBlue=(125, 255, 255)):
        # define the lower and upper boundaries of the "yellow-green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        self.greenLower = lowerColorGreen
        self.greenUpper = upperColorGreen
        self.blueLower = lowerColorBlue
        self.blueUpper = upperColorBlue
        self.vs = None
        self.args = None

    def take_video(self, args, option):
        self.args = args
        if option == 1:
            self.vs = VideoStream(src=0).start()
        else:
            self.vs = cv2.VideoCapture(args["video"])
        # allow the camera or video file to warm up
        time.sleep(2.0)

    def video_resolution(self):
        img = self.vs.read()
        height, width = img.shape[:2]
        return height, width

    def find_contours(self, option):
        # keep looping
        # grab the current frame
        self.frame = self.vs.read()
        # handle the frame from VideoCapture or VideoStream
        self.frame = self.frame[1] if self.args.get(
            "video", False) else self.frame
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if self.frame is not None:
            # resize the frame, blur it, and convert it to the HSV
            # color space
            # resizing IMO (juan) is important so we can be sure that both the
            # coordonates of the goal and the ones of the ball are properly scaled
            # self.frame = imutils.resize(self.frame, width=600)
            blurred = cv2.GaussianBlur(self.frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            if option == 1:
                mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
            else:
                mask = cv2.inRange(hsv, self.blueLower, self.blueUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            self.cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)
            self.cnts = imutils.grab_contours(self.cnts)
            self.center = None

    def detect_goal(self):
        self.find_contours(2)
        # create list to store both points
        pts = deque(maxlen=10)
        # continue only if there are contours found
        if len(self.cnts) > 0:
            # loop over the contours
            for c in self.cnts:
                # find radius
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                # find center only if radius is big enough
                if radius > 10:
                    # find center
                    M = cv2.moments(c)
                    if M["m00"] == 0:
                        M["m00"] = 0.0000001
                    self.center = (int(M["m10"] / M["m00"]),
                                   int(M["m01"] / M["m00"]))
                    pts.appendleft(self.center)
        return pts

    def __iter__(self):
        while True:
            self.find_contours(1)
            if self.frame is None:
                break
            # only proceed if at least one contour was found
            if len(self.cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(self.cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if radius >= 3:
                    self.center = (int(M["m10"] / M["m00"]),
                                   int(M["m01"] / M["m00"]))
                    cv2.circle(self.frame, (int(x), int(y)), int(radius),
                               (0, 255, 255), 2)
                    cv2.circle(self.frame, self.center, 5, (0, 0, 255), -1)
                else:
                    yield None
            # show the frame to our screen
            cv2.imshow("Frame", self.frame)
            key = cv2.waitKey(1) & 0xFF
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

            yield self.center

    def close(self):

        self.vs.release()
        # close all windows
        cv2.destroyAllWindows()
