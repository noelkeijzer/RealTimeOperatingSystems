import imageRecognizer
import picamera
import picamera.array as pa
import time
import updatedController as controller
import sys
import cv2

# define the camera and its settings
camera_resolution = (400, 300)
camera = picamera.PiCamera()
camera.rotation = 180
camera.resolution = camera_resolution
# camera.awb_mode = 'off'
# camera.awb_gains = (1.05, 1.85)

# define the parameters
inaccuracy = 0.05
stop_percentage = 0.5
resolution_middle = camera.resolution[0] / 2
stop_threshhold = 2
debug = False

# hsv threshholds
hsv_lower = (40, 80, 80)
hsv_upper = (90, 255, 255)

# define the buffer to use for picture processing
picture_buffer = pa.PiRGBArray(camera)


def init():
    global debug
    if len(sys.argv) > 1:
        print "debug set"
        debug = True
    imageRecognizer.init(debug)
    controller.init()


def get_signal(image):
    result = imageRecognizer.bottle_detection(image, hsv_lower, hsv_upper)
    if result is not None:
        (lowest_x, highest_x) = result
        middle_point = lowest_x + ((highest_x - lowest_x) / 2)
        result = middle_point - resolution_middle
        width = float((highest_x - lowest_x)) / float(camera.resolution[0])
        if width >= stop_percentage:
            return (999,width)
        else:
            return (result, width)
    else:
        print "[Processor]\t: no bottle found in picture"
        return (-999,0)


def main():
    try:
        camera.start_preview()
        time.sleep(1)
        camera.stop_preview()
        init()
        stop_counter = 0
        for frame in camera.capture_continuous(picture_buffer, format="bgr", use_video_port = True):
            image = picture_buffer.array
            (signal, width) = get_signal(image)
            picture_buffer.truncate(0)
            if signal == 999:
                stop_counter += 1
                print "[Processor]\t: stop counter = "+ str(stop_counter)
                if stop_counter >= stop_threshhold:
                    controller.control(999, width)
                    break
            else:
                stop_counter = 0
                controller.control(signal, width)
            if signal == -999:
                time.sleep(0.1)
    except:
        controller.control(999, 0)
        sys.exit(0)

if __name__ == '__main__':
    main()
