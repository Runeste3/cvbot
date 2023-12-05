import cv2 as cv
from cvbot.images import Image


def read_img(path, key="none"):
    """
    str -> Image | None
    Load a local image from disk return None if not found
    """
    try:
        if key == "none":
            img = Image(cv.imread(path))
        elif key == "grey" or key == "gray":
            img = Image(cv.imread(path, 0))

        return img
    except:
        return

def save_img(img, pth):
    """
    Image, str -> None
    Save given image to given path
    """
    cv.imwrite(pth, img.img)
