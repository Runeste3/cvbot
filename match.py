import cv2 as cv
import numpy as np
from cvbot._sift import find, show_features
from cvbot.capture import get_region
from math import dist


REGION = None

def _mse(imga, imgb):
    err = np.sum((imga.astype("float") - imgb.astype("float")) ** 2)
    err /= float(imga.shape[0] * imga.shape[1])

    return err

def _cmse(imga, imgb):
    return (_mse(imga[:, :, 0], imgb[:, :, 0]) + 
            _mse(imga[:, :, 1], imgb[:, :, 1]) +
            _mse(imga[:, :, 2], imgb[:, :, 2]))

def sift_find(temp, scene, quality):
    """
    Image, Image, int -> box
    Find using sift features of the image 'temp' in 'scene' image and return the location as a rectangle/box
            quality : minimum features to find
    """
    return find(temp.grey(),
                scene.grey(), quality)

def sift_feats(img):
    """
    Image -> None
    Show detected sift feature of 'img' in a window on screen
    """
    show_features(img.grey())

def mse(imga, imgb):
    """
    Image, Image -> float | None
    Return the mean squared difference between two images
    """
    if imga.type != imgb.type:
        print("Mean squared difference cannot be calculated with images of different color types")
    elif imga.type == "grey":
        return _mse(imga.img, imgb.img) 
    else:
        return _cmse(imga.img, imgb.img)

def compare(pos, temp, thresh=500, prnt=False): 
    """
    tuple(int, int), Image(grey), int -> bool
    Return False - Image in "pos" with the same width and height as "temp" 
                   doesn't match given "temp" Image bounded by the given thresh
           Ture  - In case of a match
    """
    region = pos + (*temp.img.shape[::-1],)
    scene = get_region(region, True)
    result = mse(temp, scene)
    if prnt:
        print(result)
        scene.show()
        temp.show()

    return result < thresh

def look_for(temp, scene=None, thresh=0.8):
    """
    Image, Image, float(0->0.1) -> tuple(int, int)
    Find a part of "scene" that matches "temp" and return it's 
        location in "scene" as (x, y)
    """
    if scene is None:
        scene = get_region(REGION, True)

    timg = temp.grey()
    simg = scene.grey()

    result = cv.matchTemplate(simg, timg, cv.TM_CCOEFF_NORMED)
    _, maxval, _, maxloc = cv.minMaxLoc(result)
    if maxval >= thresh:
        w, h = temp.size
        pos = maxloc[0] + (w//2), maxloc[1] + (h//2)
        return pos

def find_all(temp, scene=None, thresh=0.8):
    """
    Image, Image, float(0->0.1) -> tuple(int, int)
    Find a part of "scene" that matches "temp" and return all 
        locations in "scene" that has matching score higher than thresh
         as (x, y)
    """
    if scene is None:
        scene = get_region(REGION, True)

    timg = temp.grey()
    simg = scene.grey()

    result = cv.matchTemplate(simg, timg, cv.TM_CCOEFF_NORMED)

    loc = np.where(result > thresh)
    w, h = temp.size

    return [(pt[0] + (w//2), pt[1] + (h//2)) for pt in zip(*loc[::-1])]

def remove_close(lpos, how_close=10):
    indx = []
    for i, apos in enumerate(lpos):
        for j, bpos in enumerate(lpos):
            if i == j or (j in indx) or (i in indx):
                continue
            elif dist(apos, bpos) < how_close:
                indx.append(j)

    indx = tuple(set(indx))
    nlpos = []
    for i in range(len(lpos)):
        if i in indx:
            continue
        else:
            nlpos.append(lpos[i])

    return nlpos
