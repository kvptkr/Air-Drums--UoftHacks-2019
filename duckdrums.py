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

greenbounds = ([35,70,70], [70,255,255]) #green
tealbounds = ([81,70,70], [100,255,255]) #teal
#redbounds = 
#H:0-180, S:0-255, V: 0-255 

vc = cv2.VideoCapture(0)

def findBottom(pixelpoints, color):
    global g_aboveToBelow
    global t_aboveToBelow
    #print(pixelpoints[0].shape)
    #[pixelpoints[0].shape[0]-1]
    
    miny = pixelpoints[0][pixelpoints[0].shape[0]-1]
    x = pixelpoints[1][pixelpoints[0].shape[0]-1]
    print("x:",x,"y:",miny)
    if miny <= 400 and not color: #green
        g_aboveToBelow = True
    elif miny <= 400 and color: #teal
        t_aboveToBelow = True
    drumKit(x, miny, color)

def drumKit(x, miny, color):
    global g_aboveToBelow
    global t_aboveToBelow
    if not color: #green
        if (miny > 400) and (0 <= x < 160) and g_aboveToBelow:
            g_aboveToBelow = False
            _thread.start_new_thread(playSound, (1,))
        elif (miny > 400) and (160 <= x < 320) and g_aboveToBelow:
            g_aboveToBelow = False
            _thread.start_new_thread(playSound, (2,))
        elif (miny > 400) and (320 <= x < 480) and g_aboveToBelow:
            g_aboveToBelow = False
            _thread.start_new_thread(playSound, (3,))
        elif (miny > 400) and (480 <= x < 640) and g_aboveToBelow:
            g_aboveToBelow = False
            _thread.start_new_thread(playSound, (4,))
    elif color: #teal
        if (miny > 400) and (0 <= x < 160) and t_aboveToBelow:
            t_aboveToBelow = False
            _thread.start_new_thread(playSound, (1,))
        elif (miny > 400) and (160 <= x < 320) and t_aboveToBelow:
            t_aboveToBelow = False
            _thread.start_new_thread(playSound, (2,))
        elif (miny > 400) and (320 <= x < 480) and t_aboveToBelow:
            t_aboveToBelow = False
            _thread.start_new_thread(playSound, (3,))
        elif (miny > 400) and (480 <= x < 640) and t_aboveToBelow:
            t_aboveToBelow = False
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
#winsound.PlaySound('hiHat.wav', winsound.SND_FILENAME)
#winsound.PlaySound('bass.wav', winsound.SND_FILENAME)
#winsound.PlaySound('tom.wav', winsound.SND_FILENAME)

def imshowDrumsticks(img):
    kernel = np.ones((15,15),np.uint8)
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
    hsvFinal = cv2.bitwise_and(img, img, mask = mask)
    rgbFinal = cv2.cvtColor(hsvFinal, cv2.COLOR_HSV2BGR)
    rgbFinal = cv2.flip(rgbFinal, 1)
    cv2.imshow('final', rgbFinal)
    

def showColor(img, lower, upper, color):
#    lower = greenbounds[0]
#    upper = greenbounds[1]
    kernel = np.ones((15,15),np.uint8)
    lowerBnd = np.array(lower, np.uint8)
    upperBnd = np.array(upper, np.uint8)
    mask = cv2.inRange(img, lowerBnd, upperBnd)
    flippedmask = cv2.flip(mask, 1)
    flippedmask = cv2.morphologyEx(flippedmask, cv2.MORPH_OPEN, kernel)
    
    
    #hsvFinal = cv2.bitwise_and(img, img, mask = mask)
    #rgbFinal = cv2.cvtColor(hsvFinal, cv2.COLOR_HSV2BGR)
    #rgbFinal = cv2.flip(rgbFinal, 1)
    
    #cv2.imshow('duck', rgbFinal)

    pixelpoints = np.nonzero(flippedmask) #mask
    while True:
        if(pixelpoints[0].shape[0] > 100):
            findBottom(pixelpoints, color)
        else:
            return
        break
    #bottommost = tuple(ctr[ctr[:,:,1].argmax()][0])
    #print(bottommost)
    
    #drumKit(pixelpoints)
    #print(pixelpoints)


if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    #cv2.imshow("preview", frame)
    aboveToBelow = False
    rval, frame = vc.read()
    #print(frame.shape)
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imshowDrumsticks(hsvframe)
#    with Pool(5) as p:
#        p.starmap(showColor, [(hsvframe,greenbounds[0],greenbounds[1]),(hsvframe,tealbounds[0],tealbounds[1])])
    _thread.start_new_thread(showColor, (hsvframe,greenbounds[0],greenbounds[1],0))
    _thread.start_new_thread(showColor, (hsvframe,tealbounds[0],tealbounds[1],1))
    #showColor(hsvframe)
    #showColor(hsvframe, greenbounds[0], greenbounds[1])
    key = cv2.waitKey(5)
    
    if key == 27: # exit on ESC
#        winsound.PlaySound('snare.wav', winsound.SND_FILENAME)
#        winsound.PlaySound('snare.wav', winsound.SND_FILENAME)
#        winsound.PlaySound('hiHat.wav', winsound.SND_FILENAME)
#        winsound.PlaySound('bass.wav', winsound.SND_FILENAME)
#        winsound.PlaySound('tom.wav', winsound.SND_FILENAME)
        break



    
cv2.destroyAllWindows()
vc.release()