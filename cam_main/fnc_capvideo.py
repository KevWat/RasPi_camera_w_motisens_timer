#! /usr/bin/env python

import cv2
import sys

# Set Parameter value from outside
video = [0] # put /dev/video [0,2]
#video = [int(sys.argv[1])] # 0 or 2 from cameraID
# Parameter
path = 'pic/' # Picture Folder Location
width = 640
height = 480
delay = 1 # unit: Sec

def capture_camera(path,width,height):   
    pic_list = [] # return picture name
    for i in  video:
        camnum = i
        capture = cv2.VideoCapture(i) # 0 is camera device number

        if not capture.isOpened():
                sys.exit()
        while True:
                ret, frame = capture.read()
                windowsize =(width,height)
                frame = cv2.resize(frame, windowsize)
                cv2.imshow('Live_video',frame)
		# xPos, yPos, width, height = cv2.getWindowImageRect('Live_video')
		# Interapt: Keyboard "Q"
                if cv2.waitKey(delay) & 0xFF == ord('q'): 
                        break
		# Interapt: "Close Window" *Does not work for cv2 version
		#if xPos == -1 :
		#	break
cv2.destroyAllWindows()


#def check for debug
a = capture_camera(path,800,600)
print(a)


