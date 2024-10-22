#!/usr/bin/env python 3.7

__author__      = "Emerson Andrade"
__version__   = "1.0.0"
__date__   = "2023"

import numpy as np
import cv2
import sys
import datetime
import matplotlib.pyplot as plt
import get_ground_truth_data as ggtd

filenames = ["video/Tracking-group-of-three-spined-sticklebacks.mp4"]
ggtd_data = ggtd.GroundTruth()
fish_list = ggtd_data.fish_list

def start(cap, filename):
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_i = 0
    t = 0
    while cap.isOpened():
        success, img = cap.read()
        if success == True:
            c_count = 0
            colors_ = [(0, 125, 250), # orange
                      (0, 250, 250), # yellow
                      (250, 0, 0), # blue
                      (250, 0, 250), # pink
                      (125, 250, 0)] # green
            original = img.copy()
            for fish_ii in [1,2,3,4,5]:
                color_iii = colors_[c_count]
                x, y = fish_list[t][fish_ii*2-1], fish_list[t][fish_ii*2]
                radius = 7.0
                cv2.circle(original, (int(x),int(y)), radius=int(radius), color=color_iii, thickness=-1)
                cv2.putText(img=original, text='%d' % (c_count+1), org=(int(x),int(y)), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0),thickness=1)
                cv2.putText(img=original, text='frame %d' % (frame_i), org=(150, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0),thickness=3)
                c_count +=1
            cv2.imshow('original', original)
            if cv2.waitKey(1) & 0xff ==ord('q'):
                break
            t += 1
            frame_i+=1
        else:
            break

for filename in filenames:
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        print("Could not open video")
        sys.exit()
    start(cap, filename)
