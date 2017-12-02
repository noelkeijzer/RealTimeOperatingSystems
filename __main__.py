import _thread as thread
import controller
import imageProcessor
import queue


def main():
    running = True
    controller_queue = queue.Queue
    thread.start_new_thread(imageProcessor.main(controller_queue, running))
