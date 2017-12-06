import _thread as thread
import controller
import imageProcessor
import queue


def main():
    running = True
    controller_queue = queue.Queue
    try:
        thread.start_new_thread(imageProcessor.main(controller_queue, running))
        thread.start_new_thread(controller.main(controller_queue, running))
    except (KeyboardInterrupt, SystemExit):
        running = False
        print("[Thread main\t: stopping")
