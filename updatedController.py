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
    correction_counter = 0
    stop_counter = 0
    not_found_counter = 0
    while j < 500 and not stop_event.is_set():
        try:
            if not queue.empty():
                correction_counter += 1
                location = queue.get()
                print "location: " + str(location)
                if location > 0 and location < 250:
                    right_speed -= right_speed * (location / 200)
                    set_right_speed(right_speed)
                    previous_command = 1
                elif location < 0 and location > -250:
                    left_speed += left_speed * (location / 200) # += because location is a negative number. will decrease the left_speed.
                    set_left_speed(left_speed)
                    previous_command = -1
                elif location == 0:
                    correction_counter -= 1
                    if correction_counter == 0:
                        left_speed = DEFAULT_LEFT_SPEED
                        right_speed = DEFAULT_RIGHT_SPEED
                        set_left_speed(left_speed)
                        set_right_speed(right_speed)
                elif location == 999:
                    stop_counter += 1
                    if stop_counter > 5:
                        stop()
                        break
                elif location == -999:
                    not_found_counter += 1
                    if not_found_counter > 5:
                        find_bottle(queue)
                        not_found_counter = 0
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
