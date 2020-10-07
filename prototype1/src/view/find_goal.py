"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import cv2
import imutils


def show_webcam():
    cam = cv2.VideoCapture(0)
    mirror = True
    for loop in range(10):
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

    # detect cross
    # cv2.imshow('my webcam', img)


def main():
    show_webcam()


if __name__ == '__main__':
    main()
