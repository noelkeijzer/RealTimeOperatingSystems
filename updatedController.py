#1/usr/bin/python
from gopigo import *
from imageRecognizer import *
import time
import queue

DEFAULT_LEFT_SPEED = 255
DEFAULT_RIGHT_SPEED = 200

def do180():
    '''
    Turn the vehicle 180 degrees as fast as possible.
    '''
    right_rot()
    sleep(0.5)
    stop()

def main(queue, running):
    left_speed = DEFAULT_LEFT_SPEED
    right_speed = DEFAULT_RIGHT_SPEED
    do180()
    set_left_speed(left_speed)
    set_right_speed(right_speed)
    fwd()
    j = 0
    while j < 500 and running:
        location = queue.get()
        if location == 1:
            right_speed -= right_speed/20
            set_right_speed(right_speed)
        elif location == -1:
            left_speed -= left_speed/20
            set_left_speed(left_speed)
        elif location == 0:
            stop()
            break
        else:
            left_speed = DEFAULT_LEFT_SPEED
            right_speed = DEFAULT_RIGHT_SPEED
            set_left_speed(left_speed)
            set_right_speed(right_speed)
        j += 1
    print("[Thread controller]\t: stopping")
    stop()

if __name__ == '__main__':
    q = queue.Queue()
    main(q, True)
