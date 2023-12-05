from cvbot.images import Image
from cvbot.windows import get_window
from cvbot._screen import get_region as _get_region
from cvbot._screen import screenshot as _screenshot
from cvbot._screen import get_pixel  as _get_pixel


dfwin = None

def default_window(wname):
    """
    str -> None
    Set 'dfwin' global variable to the window with title 'win'
    """
    global dfwin
    dfwin = get_window(wname)

#def trim_pad(img):
#    """
#    npimage -> npimage
#    Remove extra paddings in screenshot
#    """
#    return img[1:-8, 8:-8]

def capture_window(wname=""):
    """
    str -> Image | None
    Take a screenshot of a toplevel window and return it as an Image
    return None if not found
    """
    global dfwin
    win = None

    if wname == "":
        win = dfwin
    else:
        win = get_window(wname)
    
    if not (win is None):
        return Image(_get_region(win.region))

def get_region(region, grey=False):
    """
    tuple(int, int, int, int), bool -> Image
    Return an Image of the screen of "region"
    where region is a tuple(x, y, w, h) coordinates on the screen
    Return grey image if "grey" is True else return colored image
    """
    return Image(_get_region(region, grey))

def screenshot(grey=False):
    """
    bool -> Image
    Take a full screenshot of the whole screen
    """
    return Image(_screenshot(grey))

def get_pixel(pos, grey=False):
    return _get_pixel(pos, grey)
