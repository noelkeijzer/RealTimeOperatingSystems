import sys
import cv2
import numpy as np

debug = False
output_image_name = 'output.jpg'
rectangle_color = (255, 0, 0)
line_thickness = 10

hsv = False

image1 = cv2.imread('im1.jpg', 1)
image2 = cv2.imread('im2.jpg', 1)
image3 = cv2.imread('im3.jpg', 1)
image4 = cv2.imread('im4.jpg', 1)
test_image = image1

# The color range to detect the bottle
# For the BGR format
bgr_lower = np.array([100, 60, 0], dtype="uint8")
bgr_upper = np.array([200, 180, 50], dtype="uint8")

# For the HSV format
hsv_lower = (29, 86, 6)
hsv_upper = (64, 255, 255)


def bottle_detection(image):
    return bottle_detection_hsv(image) if hsv else bottle_detection_bgr(image)


def bottle_detection_bgr(image):
    mask = cv2.inRange(image, bgr_lower, bgr_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    if debug:
        (x, y, w, h) = get_absolute_locations(mask)
        cv2.rectangle(image, (x, y), (x + w, y + h), rectangle_color, line_thickness)
        cv2.imwrite(output_image_name, image)
        return x + w / 2, h
    else:
        return get_absolute_locations(mask)


def bottle_detection_hsv(image):
    new_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(new_image, hsv_lower, hsv_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    if debug:
        (x, y, w, h) = get_absolute_locations(mask)
        cv2.rectangle(image, (x, y), (x + w, y + h), rectangle_color, line_thickness)
        cv2.imwrite(output_image_name, image)
        return x + w / 2, h
    else:
        return get_absolute_locations(mask)


def get_absolute_locations(mask):
    # Get all the pixel locations that are white in the mask
    locations = cv2.findNonZero(mask)

    lowest_x = sys.maxsize
    lowest_y = sys.maxsize
    highest_x = 0
    highest_y = 0

    # Loop through all the pixel locations and record the extremes
    for p in locations:
        x = p[0][0]
        y = p[0][1]
        if x <= lowest_x:
            lowest_x = x
        elif x >= highest_x:
            highest_x = x

        if y <= lowest_y:
            lowest_y = y
        elif y >= highest_y:
            highest_y = y

    if debug:
        # return the absolute values in the (x, y, w, h) format
        return lowest_x, lowest_y, highest_x - lowest_x, highest_y - lowest_y
    else:
        # return the middle point of the bottle and the height of the bottle
        return lowest_x + ((highest_x - lowest_x) / 2), highest_y - lowest_y


if __name__ == '__main__':
    print(bottle_detection(test_image))
