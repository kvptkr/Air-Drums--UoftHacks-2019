# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 00:12:38 2019

@author: Armaan LADak
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import _thread
import pygame as pg
#from multiprocessing import Pool
#import tesseract

pg.mixer.init()
pg.init()

a = pg.mixer.Sound("A.wav")
b = pg.mixer.Sound("B.wav")
c1 = pg.mixer.Sound("C_1.wav")
c2 = pg.mixer.Sound("C_2.wav")
d = pg.mixer.Sound("D.wav")
e = pg.mixer.Sound("E.wav")
f = pg.mixer.Sound("F.wav")
g = pg.mixer.Sound("G.wav")



pg.mixer.set_num_channels(60)

g_aboveToBelow = False
t_aboveToBelow = False

#g_hit = 0
#t_hit = 0

framecount = 0

greenbounds = ([35,70,70], [75,255,255]) #green
tealbounds = ([81,70,70], [100,255,255]) #teal

vc = cv2.VideoCapture(0)

def findBottom(pixelpoints, color):
    global g_aboveToBelow
    global t_aboveToBelow
    
    miny = pixelpoints[0][pixelpoints[0].shape[0]-1]
    x = pixelpoints[1][pixelpoints[0].shape[0]-1]
    #print("x:",x,"y:",miny)
    if miny <= 350 and not color: #green
        g_aboveToBelow = True
    elif miny <= 350 and color: #teal
        t_aboveToBelow = True
    drumKit(x, miny, color)

def drumKit(x, miny, color):
    global g_aboveToBelow
    global t_aboveToBelow
#    global g_hit
#    global t_hit
    if not color: #green
        if (miny > 350) and (0 <= x < 80) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 1
            _thread.start_new_thread(playSound, (1,))
        elif (miny > 350) and (80 <= x < 160) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 2
            _thread.start_new_thread(playSound, (2,))
        elif (miny > 350) and (160 <= x < 240) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 3
            _thread.start_new_thread(playSound, (3,))
        elif (miny > 350) and (240 <= x < 320) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 4
            _thread.start_new_thread(playSound, (4,))
        elif (miny > 350) and (320 <= x < 400) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 1
            _thread.start_new_thread(playSound, (5,))
        elif (miny > 350) and (400 <= x < 480) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 2
            _thread.start_new_thread(playSound, (6,))
        elif (miny > 350) and (480 <= x < 560) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 3
            _thread.start_new_thread(playSound, (7,))
        elif (miny > 350) and (560 <= x < 640) and g_aboveToBelow:
            g_aboveToBelow = False
#            g_hit = 4
            _thread.start_new_thread(playSound, (8,))
        
    elif color: #teal
        if (miny > 350) and (0 <= x < 80) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 1
            _thread.start_new_thread(playSound, (1,))
        elif (miny > 350) and (80 <= x < 160) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 2
            _thread.start_new_thread(playSound, (2,))
        elif (miny > 350) and (160 <= x < 240) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 3
            _thread.start_new_thread(playSound, (3,))
        elif (miny > 350) and (240 <= x < 320) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 4
            _thread.start_new_thread(playSound, (4,))
        elif (miny > 350) and (320 <= x < 400) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 1
            _thread.start_new_thread(playSound, (5,))
        elif (miny > 350) and (400 <= x < 480) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 2
            _thread.start_new_thread(playSound, (6,))
        elif (miny > 350) and (480 <= x < 560) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 3
            _thread.start_new_thread(playSound, (7,))
        elif (miny > 350) and (560 <= x < 640) and t_aboveToBelow:
            t_aboveToBelow = False
#            g_hit = 4
            _thread.start_new_thread(playSound, (8,))

def playSound(instr):
    if instr == 1:
        c1.play()
    elif instr == 2:
        d.play()
    elif instr == 3:
        e.play()
    elif instr == 4:
        f.play()
    elif instr == 5:
        g.play()
    elif instr == 6:
        a.play()
    elif instr == 7:
        b.play()
    elif instr == 8:
        c2.play()
    else:
        print("instrument code out of range")

def imshowDrumsticks(img):
#    global g_hit
#    global t_hit
    xylo = cv2.imread("xylo.png",-1)
    smallwoody = cv2.imread("smallwoody.png",-1)
    
    kernel = np.ones((14,14),np.uint8)
    g_lower = greenbounds[0]
    g_upper = greenbounds[1]
    t_lower = tealbounds[0]
    t_upper = tealbounds[1]
    
    g_lowerBnd = np.array(g_lower, np.uint8)
    g_upperBnd = np.array(g_upper, np.uint8)
    g_mask = cv2.inRange(img, g_lowerBnd, g_upperBnd)
    g_mask = cv2.morphologyEx(g_mask, cv2.MORPH_OPEN, kernel)    
    
    t_lowerBnd = np.array(t_lower, np.uint8)
    t_upperBnd = np.array(t_upper, np.uint8)
    t_mask = cv2.inRange(img, t_lowerBnd, t_upperBnd)
    t_mask = cv2.morphologyEx(t_mask, cv2.MORPH_OPEN, kernel)
    
    mask = cv2.bitwise_or(g_mask,t_mask)
    invmask = cv2.flip((255 - mask), 1)
    hsvFinal = cv2.bitwise_and(img, img, mask = mask)
    rgbFinal = cv2.cvtColor(hsvFinal, cv2.COLOR_HSV2BGR)
    rgbFinal = cv2.flip(rgbFinal, 1)
    woodymask = cv2.bitwise_and(smallwoody, smallwoody, mask = invmask)
    rgbFinal2 = cv2.bitwise_or(woodymask,rgbFinal)
    
    y1, y2 = 0, xylo.shape[0]
    x1, x2 = 0, xylo.shape[1]
    
    alpha_fg = xylo[:,:,3] / 255.0
    alpha_bg = 1.0 - alpha_fg
    for c in range(0,3):
        rgbFinal2[y1:y2, x1:x2, c] = (alpha_fg * xylo[:,:,c] + alpha_bg * rgbFinal2[y1:y2, x1:x2, c])
    

    cv2.imshow('final', rgbFinal2)

def showColor(img, lower, upper, color):
    kernel = np.ones((14,14),np.uint8)
    lowerBnd = np.array(lower, np.uint8)
    upperBnd = np.array(upper, np.uint8)
    mask = cv2.inRange(img, lowerBnd, upperBnd)
    flippedmask = cv2.flip(mask, 1)
    flippedmask = cv2.morphologyEx(flippedmask, cv2.MORPH_OPEN, kernel)

    pixelpoints = np.nonzero(flippedmask) #mask
    while True:
        if(pixelpoints[0].shape[0] > 100):
            findBottom(pixelpoints, color)
        else:
            return
        break

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    rval, frame = vc.read()
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#    if framecount % 10 == 0:
#        g_hit = 0
#        t_hit = 0
    _thread.start_new_thread(showColor, (hsvframe,greenbounds[0],greenbounds[1],0))
    _thread.start_new_thread(showColor, (hsvframe,tealbounds[0],tealbounds[1],1))
    imshowDrumsticks(hsvframe)
    framecount += 1
    key = cv2.waitKey(5)
    
    if key == 27: # exit on ESC
        break
    
cv2.destroyAllWindows()
vc.release()