import imageRecognizer
import picamera
import numpy as np

inaccuracy = 0.10
stop_percentage = 0.8
camera_resolution = (1024, 768)
resolution_middle = camera_resolution[0] / 2
camera = picamera.PiCamera()
camera.vflip = True
camera.resolution = camera_resolution


def get_signal():
    picture = np.empty((768, 1024, 3), dtype=np.uint8)
    camera.capture(picture, 'rgb')
    (middle_point, height) = imageRecognizer.bottle_detection(picture)
    if height / camera_resolution[1] >= stop_percentage:
        print "[Thread processor]\t: send stopping signal to the queue"
        return 0
    elif middle_point <= resolution_middle - camera_resolution[0] * inaccuracy:
        print "[Thread processor]\t: send go left signal to the queue"
        return -1
    elif middle_point >= resolution_middle + camera_resolution[0] * inaccuracy:
        print "[Thread processor]\t: send go right signal to the queue"
        return 1
    print "[Thread processor]\t: no bottle found in picture"
    return None


def main(queue, running):
    while running:
        signal = get_signal()
        if signal is not None:
            queue.put(get_signal())
            queue.join()

    print "[Thread processor]\t: stopping"
