import cv2
import webcolors
from imutils.video import WebcamVideoStream
import imutils

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS21_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


class Video(object):
    def __init__(self):
        self.video = WebcamVideoStream(src=0).start()
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    def __del__(self):
        self.video.stop()
    
    def get_frame(self):
        image = self.video.read()
        frame = imutils.resize(image, width= 1280, height= 720)

        width = 1280
        height = 720
        cx = int(width/2)
        cy = int(height/2)
        
        pixel_center_bgr = frame[cy, cx]
        
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
        
        requested_colour = (r,g,b)
        actual_name, closest_name = get_colour_name(requested_colour)

        if actual_name:
            color = actual_name
        else:
            color = closest_name
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, color , (cx - 200, 100), font, 2, (0,0,0), 3, lineType=cv2.LINE_AA)
        cv2.putText(frame, 'Press Home TO EXIT' , (10, 900), font, 1, (255,255,255), 3, lineType=cv2.LINE_AA)
        cv2.circle(frame, (cx, cy), 5, (255,255,255), 3)
        
        ret, jpeg = cv2.imencode('.jpg', frame)

        data = []
        data.append(jpeg.tobytes())

        return data