import numpy as np
from time import time
from random import uniform
from pynput.mouse import Controller as msctrl
from pynput.mouse import Button as msbtn
from random import randrange


# CONSTANTS
MSP = 80 
SQRT3 = np.sqrt(3)
SQRT5 = np.sqrt(5)
hmv = True 
ms = msctrl()
tl = 0, 0


#
def acc_sleep(t):
    st = time()
    while time() - st < t:
        continue

# point, *String, *float, *float, *int, *float -> None
# Given a point representing coordinates on screen 
# move the mouse and click on it
#   using either the left or right mouse button
#       btn   -> what mouse button to use (left, right)
#       hold  -> how long to hold the mouse button before releasing
#       hover -> how long to wait after moving the mouse before clicking
#       times -> click how many times
#       delay -> when clicking many times how long to wait between clicks
def click(p, btn="left", hold=0.05, hover=0.03, times=1, delay=0, quick=False):
    global hmv
    if quick:
        hmv = False 
    btn = eval("msbtn." + btn)
    move(p)
    acc_sleep(hover)

    for _ in range(times):
        ms.press(btn)
        acc_sleep(hold)
        ms.release(btn)
        acc_sleep(delay)

    hmv = True 

def click_region(reg, btn="left", hold=0.05, hover=0.03, times=1, delay=0):
    x = randrange(reg[0], reg[0] + reg[2])
    y = randrange(reg[1], reg[1] + reg[3])
    click((x, y), btn, hold, hover, times, delay)

# (int, int) -> none
# Move cursor by p[0] in the x coordintae
#                p[1] in the y coordinate
def moveby(p):
    pos = ms.position
    target = pos[0] + p[0], pos[1] + p[1]
    move(target)

# point, (int, int), String, *int -> None
# Press and hold the given mouse button from point p
# to point p + offset then release
def drag_fromby(p, offset, btn="left", hover=0.15,
                hold=0):
    btn = eval("msbtn." + btn)

    move(p)
    acc_sleep(hover)
    ms.press(btn)
    acc_sleep(hover)
    move(((p[0] + offset[0]), (p[1] + offset[1])))
    acc_sleep(hover)
    acc_sleep(hold)
    ms.release(btn)

def vdrag_fromby(p, vos, hold=0.1, hover=0.03, inbetween=0):
    btn = msbtn.left

    p = tuple(p)
    move(p)
    acc_sleep(hover)
    ms.press(btn)

    if vos > 0:
        yd = 1
    else:
        yd = -1

    np = p
    while np[1] != p[1] + vos:
        np = np[0], np[1] + yd
        acc_sleep(inbetween)
        move(np)

    acc_sleep(hold)
    ms.release(btn)

def drag_to(p, btn="left", hold=0.03):
    btn = eval("msbtn." + btn)

    ms.press(btn)
    acc_sleep(hold)
    move(p)
    acc_sleep(hold)
    ms.release(btn)

def move_by(offset):
    p = ms.position
    p = p[0] + offset[0], p[1] + offset[1]
    move(p)


# point -> None
# Move mouse cursor to point in screen
def move(p):
    p = p[0] + tl[0], p[1] + tl[1]
    if hmv:
        human_mouse(*ms.position, *p)
    else:
        ms.position = p

# int, int, int, int, *int, *int, *int, *int -> None
# Makes the mouse movement human like
#   G_0 - magnitude of the gravitational fornce
#   W_0 - magnitude of the wind force fluctuations
#   M_0 - maximum step size (velocity clip threshold)
#   D_0 - distance where wind behavior changes from random to damped
def human_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12):
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/SQRT3 + (2*np.random.random()-1)*W_mag/SQRT5
            W_y = W_y/SQRT3 + (2*np.random.random()-1)*W_mag/SQRT5
        else:
            W_x /= SQRT3
            W_y /= SQRT3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= SQRT5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            ms.position = (current_x:=move_x, current_y:=move_y)

        wait = uniform(0, (100/MSP)) * 6
        
        if wait < (100 / MSP):
            wait = (100 / MSP)
            
        wait = (wait*0.9)/1000
        
        acc_sleep(wait)

def random_move():
    """
    None -> None
    Move the mouse to a random location on screen
    """
    p = randrange(100, 1800), randrange(100, 900)
    move(p)

