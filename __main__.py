import threading
import updatedController
import imageProcessor
import Queue
import time
import sys


def main():
    stop = threading.Event()
    try:
        controller_queue = Queue.Queue()

        # define the two threads
        image_thread = threading.Thread(target=imageProcessor.main, args=(controller_queue,stop))
        controller_thread = threading.Thread(target=updatedController.main, args=(controller_queue,stop))

        # start the two threads
        image_thread.start()
        controller_thread.start()

        # wait for the two threads to finish
        while image_thread.is_alive() or controller_thread.is_alive():
            time.sleep(0.5)

        print "[Thread main\t: stopping"
    except (KeyboardInterrupt, SystemExit):
        print "exception occurred"
        stop.set()
        sys.exit(0)


if __name__ == '__main__':
    main()
