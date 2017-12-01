import numpy as np
import cv2
import sys

import time

hsv = False
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

image1 = cv2.imread('im1.jpg', 1)
image2 = cv2.imread('im2.jpg', 1)
image3 = cv2.imread('im3.jpg', 1)
image4 = cv2.imread('im4.jpg', 1)
image = image1
mask = None

if hsv:
    new_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(new_image, greenLower, greenUpper)
else:
    lower = np.array([100, 60, 0], dtype="uint8")
    upper = np.array([200, 180, 50], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)

mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
# contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

# cv2.drawContours(image, contours, -1, (255,0,0),10)
# cv2.imwrite("output.jpg", image)

left_high = [sys.maxsize, sys.maxsize]

right_low = [0, 0]

locations = cv2.findNonZero(mask)
for p in locations:
    x = p[0][0]
    y = p[0][1]
    if x <= left_high[0]:
        left_high[0] = x
    elif x >= right_low[0]:
        right_low[0] = x

    if y <= left_high[1]:
        left_high[1] = y
    elif y >= right_low[1]:
        right_low[1] = y
cv2.rectangle(image, (left_high[0], left_high[1]), (right_low[0], right_low[1]), (255, 0, 0), 10)
cv2.imwrite('output.jpg', image)
