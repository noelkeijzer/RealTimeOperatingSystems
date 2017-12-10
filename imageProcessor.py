import imageRecognizer
import picamera
import picamera.array as pa
import Queue

# define the camera and its settings
camera_resolution = (1024, 768)
camera = picamera.PiCamera()
camera.rotation = 180
camera.resolution = camera_resolution

# define the parameters
inaccuracy = 0.10
stop_percentage = 0.8
resolution_middle = camera_resolution[0] / 2

# define the buffer to use for picture processing
picture_buffer = pa.PiRGBArray(camera)


def get_signal():
    camera.capture(picture_buffer, format='bgr')
    picture_array = picture_buffer.array
    result = imageRecognizer.bottle_detection(picture_array)
    picture_buffer.truncate(0)
    if result is not None:
        (middle_point, height) = result
        if height / camera_resolution[1] >= stop_percentage:
            print "[Thread processor]\t: send stopping signal to the queue"
            return 0
        elif middle_point <= resolution_middle - camera_resolution[0] * inaccuracy:
            print "[Thread processor]\t: send go left signal to the queue"
            return -1
        elif middle_point >= resolution_middle + camera_resolution[0] * inaccuracy:
            print "[Thread processor]\t: send go right signal to the queue"
            return 1
    else:
        print "[Thread processor]\t: no bottle found in picture"
        return result


def main(queue):
    signal = get_signal()
    while signal is not 0:
        if signal is not None:
            queue.put(signal)
            queue.join()
        signal = get_signal()

    print "[Thread processor]\t: stopping"


if __name__ == '__main__':
    q = Queue.Queue()
    main(q)
