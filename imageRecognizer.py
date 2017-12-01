# import the necessary packages
import numpy as np
import cv2
import sys

image1 = cv2.imread('im1.jpg', 1)
image2 = cv2.imread('im2.jpg', 1)
image3 = cv2.imread('im3.jpg', 1)
image4 = cv2.imread('im4.jpg', 1)
image = image1

lower = np.array([100, 60, 0], dtype="uint8")
upper = np.array([200, 180, 50], dtype="uint8")

# find the colors within the specified boundaries and apply
# the mask
mask = cv2.inRange(image, lower, upper)

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
cv2.imwrite('output.jpg', mask)
cv2.waitKey(0)
