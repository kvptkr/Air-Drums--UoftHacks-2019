# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 00:12:38 2019

@author: Armaan LADak
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import winsound
import _thread
import pygame as pg
#import tesseract

pg.mixer.init()
pg.init()

tom = pg.mixer.Sound("tom.wav")
bass = pg.mixer.Sound("bass.wav")
hiHat = pg.mixer.Sound("hiHat.wav")
snare = pg.mixer.Sound("snare.wav")

pg.mixer.set_num_channels(50)

aboveToBelow = True
#greenbounds = ([35,70,70], [80,255,255])
greenbounds = ([165,120,40], [180,255,255])
#redbounds = 
#H:0-180, S:0-255, V: 0-255 

vc = cv2.VideoCapture(0)

def findBottom(pixelpoints):
    global aboveToBelow
    #print(pixelpoints[0].shape)
    #[pixelpoints[0].shape[0]-1]
    
    miny = pixelpoints[0][pixelpoints[0].shape[0]-1]
    print(miny)
    if miny <= 400:
        aboveToBelow = True
    drumKit(miny)

def drumKit(miny):
    global aboveToBelow
    if miny > 400 and aboveToBelow:
        aboveToBelow = False
        print("bong")
        _thread.start_new_thread(playSound, (1,))
        
    #elif for rest of sounds. Add x coord

def playSound(instr):
    if instr == 1:
        tom.play()
    elif instr == 2:
        bass.play()
    elif instr == 3:
        hiHat.play()
    elif instr == 4:
        snare.play()
    else:
        print("instrument code out of range")
#winsound.PlaySound('hiHat.wav', winsound.SND_FILENAME)
#winsound.PlaySound('bass.wav', winsound.SND_FILENAME)
#winsound.PlaySound('tom.wav', winsound.SND_FILENAME)


def showColor(img, ):
    lower = greenbounds[0]
    upper = greenbounds[1]
    lowerBnd = np.array(lower, np.uint8)
    upperBnd = np.array(upper, np.uint8)
    mask = cv2.inRange(img, lowerBnd, upperBnd)
    flippedmask = cv2.flip(mask, 1)
    
    
    hsvFinal = cv2.bitwise_and(img, img, mask = mask)
    rgbFinal = cv2.cvtColor(hsvFinal, cv2.COLOR_HSV2BGR)
    rgbFinal = cv2.flip(rgbFinal, 1)
    
    cv2.imshow('duck', rgbFinal)
    pixelpoints = np.nonzero(flippedmask) #mask
    while True:
        if(pixelpoints[0].shape[0] > 100):
            findBottom(pixelpoints)
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
    rval, frame = vc.read()
    #print(frame.shape)
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    showColor(hsvframe)
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