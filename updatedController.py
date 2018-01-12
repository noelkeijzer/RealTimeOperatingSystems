# /usr/bin/python
from gopigo import *
from imageRecognizer import *
import time
import Queue
import sys
import signal
import threading

DEFAULT_LEFT_SPEED = 110
DEFAULT_RIGHT_SPEED = 100.0
CORRECTION_GRADIENT = 1750.0
LOCATING_THRESHOLD = 5
left_speed = DEFAULT_LEFT_SPEED
right_speed = DEFAULT_RIGHT_SPEED
stop_counter = 0


def do180():
    '''
    Turn the vehicle 180 degrees as fast as possible.
    '''
    right_rot()
    time.sleep(0.8)
    print "[Controller]\t: did 180"
    stop()
    print "[Controller]\t: stopped after 180"


def set_speed():
    set_right_speed(int(right_speed))
    set_left_speed(int(left_speed))
    fwd()


def init():
    do180()
    set_speed()


def control(location, width):
    global right_speed
    global left_speed
    global stop_counter
    print "[Controller]\t: location: " + str(location)
    if location > 20 and location < 250:
        right_speed -= right_speed * ((float(location) / CORRECTION_GRADIENT) * 2.5 * width)
        left_speed = DEFAULT_LEFT_SPEED
        print "[Controller]\t: updated right speed: " + str(right_speed)
        set_speed()
    elif location < -20 and location > -250:
        right_speed = DEFAULT_RIGHT_SPEED
        left_speed += left_speed * ((float(location) / CORRECTION_GRADIENT) * 2 * width)  #+= because this will result in a negative number
        print "[Controller]\t: updated left speed: " + str(left_speed)
        set_speed()
    elif location < 20 and location > -20 and (left_speed != DEFAULT_LEFT_SPEED or right_speed != DEFAULT_RIGHT_SPEED):
        left_speed = DEFAULT_LEFT_SPEED
        right_speed = DEFAULT_RIGHT_SPEED
        set_speed()
    elif location == 999:
        print "[Controller]\t: received stop signal, calling stop."
        stop()
    elif location == -999:
        right_rot()
        time.sleep(0.1)
        stop()

