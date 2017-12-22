import sys
import cv2
import numpy as np

debug = True
rectangle_color = (0, 0, 255)
line_thickness = 5

def bottle_detection(image, hsv_lower, hsv_upper):
    new_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(new_image, hsv_lower, hsv_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    return write_image(image, mask) if debug else get_absolute_locations(mask)


def write_image(image, mask):
    result = get_absolute_locations(mask)

    if result is not None:
        (x, y, w, h) = result
        cv2.rectangle(image, (x, y), (x + w, y + h), rectangle_color, line_thickness)
        cv2.imshow('video', image)
        cv2.waitKey(1)
        return x, x + w
    else:
        cv2.imshow('video', image)
        cv2.waitKey(1)
        return None


def get_absolute_locations(mask):
    # Get all the pixel locations that are white in the mask
    locations = cv2.findNonZero(mask)
    lowest_x = sys.maxsize
    lowest_y = sys.maxsize
    highest_x = 0
    highest_y = 0

    # Loop through all the pixel locations and record the extremes
    if locations is not None:
        for p in locations:
            x = p[0][0]
            y = p[0][1]
            if x <= lowest_x:
                lowest_x = x
            
            if x >= highest_x:
                highest_x = x

            if y <= lowest_y:
                lowest_y = y
            
            if y >= highest_y:
                highest_y = y

        if debug:
            # return the absolute values in the (x, y, w, h) format
            return lowest_x, lowest_y, highest_x - lowest_x, highest_y - lowest_y
        else:
            # return the x values
            return lowest_x, highest_x
    else:
        return None


if __name__ == '__main__':
    print(bottle_detection(test_image))
