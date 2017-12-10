import threading
import controller
import imageProcessor
import Queue


def main():
    controller_queue = Queue.Queue()

    # define the two threads
    image_thread = threading.Thread(target=imageProcessor.main, args=controller_queue)
    controller_thread = threading.Thread(target=controller.main, args=controller_queue)

    # start the two threads
    image_thread.start()
    controller_thread.start()

    # wait for the two threads to finish
    image_thread.join()
    controller_thread.join()

    print "[Thread main\t: stopping"


if __name__ == '__main__':
    main()
