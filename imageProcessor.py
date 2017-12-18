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
resolution_middle = camera_resolution[0] / 2

# define the buffer to use for picture processing
picture_buffer = pa.PiRGBArray(camera)


def get_signal(image):
    result = imageRecognizer.bottle_detection(image)
    if result is not None:
        print result
        (lowest_x, highest_x) = result
        middle_point = lowest_x + (highest_x - lowest_x / 2)
        if (highest_x - lowest_x) / camera_resolution[1] >= stop_percentage:
            print "[Thread processor]\t: send stopping signal to the queue"
            return 0
        elif middle_point <= resolution_middle - camera_resolution[0] * inaccuracy:
            print "[Thread processor]\t: send go left signal to the queue"
            return middle_point - resolution_middle
        elif middle_point >= resolution_middle + camera_resolution[0] * inaccuracy:
            print "[Thread processor]\t: send go right signal to the queue"
            return middle_point - resolution_middle
    else:
        print "[Thread processor]\t: no bottle found in picture"
        return result


def main(queue,stop):
    global camera
    camera.start_preview()
    time.sleep(1)
    camera.stop_preview()
    for frame in camera.capture_continuous(picture_buffer, format="bgr", use_video_port = True):
        image = picture_buffer.array
        signal = get_signal(image)
        picture_buffer.truncate(0)
        if signal is not 0 and not stop.is_set():
            if signal is not None:
                queue.put(signal)
                # queue.join()
        else:
            break
    print "[Thread processor]\t: stopping"


if __name__ == '__main__':
    q = Queue.Queue()
    main(q,threading.Event())
