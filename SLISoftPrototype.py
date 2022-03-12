#pycaw code

import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from  pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

import screen_brightness_control as sbc

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeInfo = volume.GetVolumeRange()
minVolume = volumeInfo[0]
maxVolume = volumeInfo[1]

#minBright = 0
#maxBright = 100


cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
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
                
                if idx == 4:
                    thumbPoint = (cx,cy)
                if idx == 8:
                    indexPoint = (cx,cy)
                if idx == 20:
                    pinkyFPoint = (cx,cy)

        cv2.circle(img, indexPoint, 10, (0,250,0), cv2.FILLED)
        cv2.circle(img, thumbPoint, 10, (10,250,250), cv2.FILLED)
        cv2.circle(img, pinkyFPoint, 10, (250,250,0), cv2.FILLED)
        
        #cv2.line(img, indexPoint, thumbPoint,(255,255,0), 2)

        length1 = math.sqrt(((indexPoint[0] - thumbPoint[0])**2)+((indexPoint[1]-thumbPoint[1])**2))# vol control
        
        length2 = math.sqrt(((pinkyFPoint[0] - thumbPoint[0])**2)+((pinkyFPoint[1]-thumbPoint[1])**2))# brightness control
        #print(length2)
        
        vol = np.interp(length1, [30,200], [minVolume, maxVolume])
        
        brigh = np.interp(length2, [20,300], [0, 100])
        
        #print(vol)

        volume.SetMasterVolumeLevel(vol,None)
        set_the_brightness = sbc.set_brightness(brigh)
                
     
    cv2.imshow("Hand Gesture", img)
    cv2.waitKey(1)
