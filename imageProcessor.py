import imageRecognizer
import picamera
import picamera.array as pa
import Queue
import threading
import time

# define the camera and its settings
camera_resolution = (400, 300)
camera = picamera.PiCamera()
camera.rotation = 180
camera.resolution = camera_resolution

# define the parameters
inaccuracy = 0.05
stop_percentage = 0.8
resolution_middle = camera.resolution[0] / 2

# hsv threshholds
hsv_lower = (40, 60, 6)
hsv_upper = (90, 250, 200)

# define the buffer to use for picture processing
picture_buffer = pa.PiRGBArray(camera)


def get_signal(image):
    result = imageRecognizer.bottle_detection(image, hsv_lower, hsv_upper)
    if result is not None:
        (lowest_x, highest_x) = result
        middle_point = lowest_x + ((highest_x - lowest_x) / 2)
        result = middle_point - resolution_middle
        if float((highest_x - lowest_x)) / float(camera.resolution[0]) >= stop_percentage:
            print "[Thread processor]\t: send stopping signal to the queue"
            return 999
        else:
            print "[Thread processor]\t: send " + str(result) + " to the queue"
            return result
    else:
        print "[Thread processor]\t: no bottle found in picture"
        return -999


def main(queue,stop):
    global camera
    camera.start_preview()
    time.sleep(1)
    camera.stop_preview()
    for frame in camera.capture_continuous(picture_buffer, format="bgr", use_video_port = True):
        image = picture_buffer.array
        signal = get_signal(image)
        picture_buffer.truncate(0)
        if signal is not None and not stop.is_set():
            queue.put(signal)
            queue.join()
        else:
            break
    print "[Thread processor]\t: stopping"


if __name__ == '__main__':
    q = Queue.Queue()
    main(q,threading.Event())
