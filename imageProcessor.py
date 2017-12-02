import imageRecognizer
import picamera
import numpy as np

inaccuracy = 0.05
stop_percentage = 0.8
camera_resolution = (1024, 768)
camera = picamera.PiCamera()
camera.vflip = True


def get_signal():
    picture = np.empty((768, 1024, 3), dtype=np.uint8)
    camera.capture(picture, 'rgb')
    (middle_point, height) = imageRecognizer.bottle_detection(picture)
    if height / camera_resolution[1] >= 0.8:
        return 1
    elif middle_point <= camera_resolution[0] - camera_resolution[0] * inaccuracy:
        return 2
    elif middle_point >= camera_resolution[0] + camera_resolution[0] * inaccuracy:
        return 3


def main(queue, running):
    while running:
        signal = get_signal()
        if signal is not None:
            queue.put(get_signal())
            queue.join()
