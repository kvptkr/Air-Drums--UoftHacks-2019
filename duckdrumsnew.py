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

cymbal = pg.mixer.Sound("cymbal.wav")
bass = pg.mixer.Sound("bass.wav")
snare = pg.mixer.Sound("snare.wav")
hiHat = pg.mixer.Sound("hiHat.wav")

pg.mixer.set_num_channels(50)

g_aboveToBelow = False
t_aboveToBelow = False

g_hit = 0
t_hit = 0

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
    if miny <= 250 and not color: #green
        g_aboveToBelow = True
    elif miny <= 250 and color: #teal
        t_aboveToBelow = True
    drumKit(x, miny, color)

def drumKit(x, miny, color):
    global g_aboveToBelow
    global t_aboveToBelow
    global g_hit
    global t_hit
    if not color: #green
        if (miny > 250) and (0 <= x < 160) and g_aboveToBelow:
            g_aboveToBelow = False
            g_hit = 1
            _thread.start_new_thread(playSound, (1,))
        elif (miny > 250) and (160 <= x < 320) and g_aboveToBelow:
            g_aboveToBelow = False
            g_hit = 2
            _thread.start_new_thread(playSound, (2,))
        elif (miny > 250) and (320 <= x < 480) and g_aboveToBelow:
            g_aboveToBelow = False
            g_hit = 3
            _thread.start_new_thread(playSound, (3,))
        elif (miny > 250) and (480 <= x < 640) and g_aboveToBelow:
            g_aboveToBelow = False
            g_hit = 4
            _thread.start_new_thread(playSound, (4,))
    elif color: #teal
        if (miny > 250) and (0 <= x < 160) and t_aboveToBelow:
            t_aboveToBelow = False
            t_hit = 1
            _thread.start_new_thread(playSound, (1,))
        elif (miny > 250) and (160 <= x < 320) and t_aboveToBelow:
            t_aboveToBelow = False
            t_hit = 2
            _thread.start_new_thread(playSound, (2,))
        elif (miny > 250) and (320 <= x < 480) and t_aboveToBelow:
            t_aboveToBelow = False
            t_hit = 3
            _thread.start_new_thread(playSound, (3,))
        elif (miny > 250) and (480 <= x < 640) and t_aboveToBelow:
            t_aboveToBelow = False
            t_hit = 4
            _thread.start_new_thread(playSound, (4,))

def playSound(instr):
    if instr == 1:
        cymbal.play()
    elif instr == 2:
        bass.play()
    elif instr == 3:
        snare.play()
    elif instr == 4:
        hiHat.play()
    else:
        print("instrument code out of range")

def imshowDrumsticks(img):
    global g_hit
    global t_hit
    drumKit = cv2.imread("before.png",-1)
    smallwoody = cv2.imread("smallwoody.png",-1)
    boom = cv2.imread("boom.png", -1)
    crash = cv2.imread("crash.png", -1)
    
    kernel = np.ones((10,10),np.uint8)
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
    
    y1, y2 = 0, drumKit.shape[0]
    x1, x2 = 0, drumKit.shape[1]
    
    alpha_fg = drumKit[:,:,3] / 255.0
    alpha_bg = 1.0 - alpha_fg
    for c in range(0,3):
        rgbFinal2[y1:y2, x1:x2, c] = (alpha_fg * drumKit[:,:,c] + alpha_bg * rgbFinal2[y1:y2, x1:x2, c])
    
    if g_hit == 1 or t_hit == 1:
        y1, y2 = 250, 250+crash.shape[0]
        x1, x2 = 0, crash.shape[1]
        
        alpha_fg = crash[:,:,3] / 255.0
        alpha_bg = 1.0 - alpha_fg
        for c in range(0,3):
            rgbFinal2[y1:y2, x1:x2, c] = (alpha_fg * crash[:,:,c] + alpha_bg * rgbFinal2[y1:y2, x1:x2, c])
    if g_hit == 2 or t_hit == 2:
        y1, y2 = 250, 250+boom.shape[0]
        x1, x2 = 160, 160+boom.shape[1]
        
        alpha_fg = boom[:,:,3] / 255.0
        alpha_bg = 1.0 - alpha_fg
        for c in range(0,3):
            rgbFinal2[y1:y2, x1:x2, c] = (alpha_fg * boom[:,:,c] + alpha_bg * rgbFinal2[y1:y2, x1:x2, c])
    if g_hit == 3 or t_hit == 3:
        y1, y2 = 250, 250+boom.shape[0]
        x1, x2 = 320, 320+boom.shape[1]
        
        alpha_fg = boom[:,:,3] / 255.0
        alpha_bg = 1.0 - alpha_fg
        for c in range(0,3):
            rgbFinal2[y1:y2, x1:x2, c] = (alpha_fg * boom[:,:,c] + alpha_bg * rgbFinal2[y1:y2, x1:x2, c])
    if g_hit == 4 or t_hit == 4:
        y1, y2 = 250, 250+crash.shape[0]
        x1, x2 = 480, 480+crash.shape[1]
        
        alpha_fg = crash[:,:,3] / 255.0
        alpha_bg = 1.0 - alpha_fg
        for c in range(0,3):
            rgbFinal2[y1:y2, x1:x2, c] = (alpha_fg * crash[:,:,c] + alpha_bg * rgbFinal2[y1:y2, x1:x2, c])

    cv2.imshow('final', rgbFinal2)

def showColor(img, lower, upper, color):
    kernel = np.ones((10,10),np.uint8)
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
    if framecount % 10 == 0:
        g_hit = 0
        t_hit = 0
    _thread.start_new_thread(showColor, (hsvframe,greenbounds[0],greenbounds[1],0))
    _thread.start_new_thread(showColor, (hsvframe,tealbounds[0],tealbounds[1],1))
    imshowDrumsticks(hsvframe)
    framecount += 1
    key = cv2.waitKey(5)
    
    if key == 27: # exit on ESC
        break
    
cv2.destroyAllWindows()
vc.release()