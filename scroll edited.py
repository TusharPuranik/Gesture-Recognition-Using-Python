#pycaw code
from pynput.mouse import Button, Controller

import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from  pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


mouse=Controller()


cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
    status, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    multiLandmarks = results.multi_hand_landmarks
    #print(multiLandmarks)
    if multiLandmarks:
        
        indexPoint = ()
        thumbPoint = ()
        pinkyFPoint = ()
        
        
        for handLms in multiLandmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for idx,lm in enumerate(handLms.landmark):
                #print(idx,lm)
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id,cx,cy)
               

                
               
                
                if idx == 12:
                    midpoint = (cx,cy)
        cv2.circle(img, midpoint, 10, (0,250,0), cv2.FILLED) 
       # cv2.circle(img, thumbPoint, 10, (10,250,250), cv2.FILLED)
       # cv2.circle(img, pinkyFPoint, 10, (250,250,0), cv2.FILLED)

           
       
        mouse.scroll(cx,cy
                     )
      
               
        
        #cv2.line(img, midpoint, thumbPoint,(255,255,0), 2)

                       
     
    cv2.imshow("Hand Gesture", img)
    cv2.waitKey(1)
