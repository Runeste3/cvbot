import mss
import numpy as np
from cv2 import cvtColor, COLOR_BGR2GRAY
from cvbot.windows import get_window_region


sct = mss.mss()
MON = sct.monitors[1]
capture = lambda rect: sct.grab(rect)

# None -> image
# Return a screenshot
def screenshot(grey):
    img = np.array(capture(MON))

    if grey:
        img = cvtColor(img, COLOR_BGR2GRAY)

    return img

# rect -> image
# Return part of a screenshot specified by rect
def get_region(rect, gry=False):
    # convert to mss notation
    rect = {"left":rect[0], "top":rect[1],
            "width":rect[2], "height":rect[3]}

    img = np.array(capture(rect))

    if gry:
        img = cvtColor(img, COLOR_BGR2GRAY)

    return img

# Point -> colors tuple 
# Return part of a screenshot specified by rect
def get_pixel(pos, gry=False):
    # convert to mss notation
    rect = {"left":pos[0], "top":pos[1],
            "width":1, "height":1}

    img = np.array(capture(rect))

    if gry:
        img = cvtColor(img, COLOR_BGR2GRAY)

    return img[0, 0]

# image, rect -> image
# Cut a region rect from given image img
def crop(img, rect):
    x1, y1, x2, y2 = rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]
    return img[y1:y2, x1:x2]

# str -> image
# Return a screenshot of the window with name "wname"
#def get_window(wname):
#    region = get_window_region(wname)
#    return get_region(region)

# None -> (int, int)
# Return (width, height) of the current monitor
def mon_size():
    return MON["width"], MON["height"]
