# /usr/bin/python
from gopigo import *
from imageRecognizer import *
import time
import Queue
import sys
import signal
import threading

DEFAULT_LEFT_SPEED = 127
DEFAULT_RIGHT_SPEED = 100

def do180():
    '''
    Turn the vehicle 180 degrees as fast as possible.
    '''
    right_rot()
    time.sleep(0.5)
    print "did 180"
    stop()
    print "stopped after 180"


def find_bottle(queue):
    time.sleep(0.25)
    while queue.empty():
        right_rot()
        time.sleep(0.15)
        stop()
        time.sleep(0.25)


def main(queue,stop_event):
    left_speed = DEFAULT_LEFT_SPEED
    right_speed = DEFAULT_RIGHT_SPEED
    do180()
    print "after 180 main"
    find_bottle(queue)
    print "Bottle has been found"
    set_left_speed(left_speed)
    set_right_speed(right_speed)
    print "set speeds"
    fwd()
    print "called forward"
    j = 0
    previous_command = 2
    while j < 500 and not stop_event.is_set():
        try:
            if not queue.empty():
                location = queue.get()
                if location == 1:
                    if previous_command == 1:
                        right_speed -= right_speed / 5
                    else:
                        right_speed -= right_speed / 10
                    set_right_speed(right_speed)
                    previous_command = 1
                elif location == -1:
                    if previous_command == -1:
                        left_speed -= left_speed / 5
                    else:
                        left_speed -= left_speed / 10
                    set_left_speed(left_speed)
                    previous_command = -1
                elif location == 0:
                    stop()
                    break
            else:
                if previous_command = 2:
                    left_speed = DEFAULT_LEFT_SPEED
                    right_speed = DEFAULT_RIGHT_SPEED
                    set_left_speed(left_speed)
                    set_right_speed(right_speed)
                previous_command = 2
            j += 1
        except:
            print "exception occurred, terminating program."
            stop()
            sys.exit(0)
    print "[Thread controller]\t: stopping"
    stop()


if __name__ == '__main__':
    q = Queue.Queue()
    main(q,threading.Event())
