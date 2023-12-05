import cv2 as cv
import numpy as np
from cvbot.images import Image


def _var(clr, variation, ln, key):
    """
    tuple(int, int, int), int -> int | tuple(int, int, int)
    Helper function
    """
    if ln == 0:
        if key == "lwr":
            total = clr - variation
            return total if total > 0 else 0
        else:
            total = clr + variation
            return total if total < 256 else 255
    else:
        nclrs = []

        for c in clr:
            if key == "lwr":
                total = c - variation
                if total > 0:
                    nclrs.append(total)
                else:
                    nclrs.append(0)
            else:
                total = c + variation
                if total < 256:
                    nclrs.append(total)
                else:
                    nclrs.append(255)

        if ln > 3:
            nclrs.append(255)

        return np.array(nclrs)

def _lwr_var(clr, variation, ln):
    """
    tuple(int, int, int), int, int -> int | tuple(int, int, int)
    Return the lower bound of the color range variation
    """
    return _var(clr, variation, ln, "lwr")

def _upr_var(clr, variation, ln):
    """
    tuple(int, int, int), int, int -> int | tuple(int, int, int)
    Return the upper bound of the color range variation
    """
    return _var(clr, variation, ln, "upr")

def count_clr(img, clr, variation=0):
    """
    Image, int | tuple(int, int, int), int -> int
    Count the number of occurances of the given color
    with the selected variation
    """
    ln = 0 if len(img.img.shape) < 3 else img.img.shape[2]

    dst = cv.inRange(img.img, 
                     _lwr_var(clr, variation, ln), 
                     _upr_var(clr, variation, ln))

    dst[dst == 255] = 1
    return dst.sum()

def threshold(img, clr, variation=0):
    """
    Image, int | tuple(int, int, int), int -> Binary Image
    Threshold a colored or grey image by a certain color or range and return
    a thresholded binary image
    """
    ln = 0 if len(img.img.shape) < 3 else img.img.shape[2]

    if not (clr is None):
        dst = cv.inRange(img.img, 
                        _lwr_var(clr, variation, ln), 
                        _upr_var(clr, variation, ln))
    else:
        _, dst = cv.threshold(img.grey(), 0, 255, cv.THRESH_OTSU) 

    return Image(dst)

def locations(img, clr, variation=0, min_area=0, min_ht=0, min_wd=0):
    """
    Image, int | tuple(int, int, int, int), int, int -> list(tuple(int, int, int, int))
    Return the locations of where the given color is concentrated as a region/box(x, y, w, h)
    """
    ln = 0 if len(img.img.shape) < 3 else img.img.shape[2]

    dst = cv.inRange(img.img, 
                     _lwr_var(clr, variation, ln), 
                     _upr_var(clr, variation, ln))

    cnts, _ = cv.findContours(dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if min_area:
        cnts = list(filter(lambda x: cv.contourArea(x) > min_area, cnts))

    cnts = [cv.boundingRect(cnt) for cnt in cnts]

    if min_ht:
        cnts = list(filter(lambda x: x[3] > min_ht, cnts))

    if min_wd:
        cnts = list(filter(lambda x: x[2] > min_wd, cnts))

    return cnts
