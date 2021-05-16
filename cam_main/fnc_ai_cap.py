# -*- coding: utf-8 -*-
# test_ai_cap.py
# CAT decision from USB camera capture image
# print"CAT exist: File Name", "CAT none-exist: File Name"
import cv2
import numpy as np

import argparse # Set command option "argparse"
import random
import time

#import fnc_cap_img_opcv_2camera as cap_opcv # 2 Camera Capture

########################
# Picture Folder Location
path = 'pic/'

'''
# for Debug
# Capture from Camera
capd_img_list = []
capd_img_list = cap_opcv.capture_camera(path, 640, 480) # Argument(Save Location,Width, Height), return: captured file name
'''

def ai_obj_det(capd_img_list):
        # Input Image Size into AI model
        IN_WIDTH = 300 # have to fix 300x300
        IN_HEIGHT = 300
        frame_width = 640
        frame_height = 480
        # Defined Label list of Studied Model (Mobilenet SSD COCO)
        CLASS_LABELS = {0: 'background',
                1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle',
                5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat',
                10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign',
                14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
                18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant',
                23: 'bear', 24: 'zebra', 25: 'giraffe', 27: 'backpack',
                28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase',
                34: 'frisbee', 35: 'skis', 36: 'snowboard', 37: 'sports ball',
                38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
                41: 'skateboard', 42: 'surfboard', 43: 'tennis racket',
                44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork',
                49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana',
                53: 'apple', 54: 'sandwich', 55: 'orange', 56: 'broccoli',
                57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
                61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant',
                65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv',
                73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard',
                77: 'cell phone', 78: 'microwave', 79: 'oven', 80: 'toaster',
                81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
                86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier',
                90: 'toothbrush'}
        # Define "Argument(Set Command Option)"
        ap = argparse.ArgumentParser()
        ap.add_argument('-p', '--pbtxt', required = True, help = 'path to pbtxt file')
        ap.add_argument('-w', '--weights', required = True, help = 'path to TensorFlow inference graph')
        ap.add_argument('-c', '--confidence', type = float, default= 0.3, help = 'minimum probability')
        ap.add_argument('-i', '--interval', type = float, default = 0, help = 'process interval to reduce CPU usage')
        args = vars(ap.parse_args())
        
        # Stop watch function from OpenCV as tm
        # kW: may not necesary
        tm = cv2.TickMeter()
        colors = {}
        # Random set on frame color for each label
        random.seed()
        
        for key in CLASS_LABELS.keys():
                colors[key] = (random.randrange(255),random.randrange(255),random.randrange(255))
        # Loading AI model
        print('Loading AI Model...')
        net = cv2.dnn.readNet(args['weights'], args['pbtxt'])
        
        for j in range(len(capd_img_list)):
                image = cv2.imread(capd_img_list[j])
                # convert to blob format from modified iputimage
                blob =  cv2.dnn.blobFromImage(image, size=(IN_WIDTH, IN_HEIGHT), swapRB=False, crop=False)
                # Set captured image into AImodel set as blob format
                net.setInput(blob)
                # Load image into AI
                tm.reset()
                tm.start()
                detections = net.forward() # Load Image into AI model(net = cv2.dnn.readNet)
                tm.stop()
                # Repeat detection
                for i in range(detections.shape[2]):
                        # pick up "i"th detected object's correct answer ratio
                        confidence = detections[0, 0, i, 2]
                        # will not do nothing, if lower than correct answer ratio
                        if confidence < args['confidence']:
                                continue
                        # Obtain Type and (x,y) of detected object
                        class_id = int(detections[0,0,i,1])
                        start_x = int(detections[0,0,i,3] * frame_width)
                        start_y = int(detections[0,0,i,4] * frame_height)
                        end_x = int(detections[0,0,i,5] * frame_width)
                        end_y = int(detections[0,0,i,6] * frame_height)
                        
                        # Set the Name label like "peroson","cat" to detemin object name
                        label = CLASS_LABELS[class_id]
                        label += ': ' + str(round(confidence * 100, 2)) + '%'
                        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                        
                        # Draw rectangle in the image
                        if CLASS_LABELS[class_id] == 'person' : # Person or not
                                #cv2.rectangle(image, (start_x, start_y), (end_x, end_y), colors[class_id], -1) # thickness : -1 patinted
                                cv2.rectangle(image, (start_x, start_y), (end_x, end_y), colors[class_id], 2) # thickness : -1 patinted
                        else :
                                cv2.rectangle(image, (start_x, start_y), (end_x, end_y), colors[class_id], 2) # thickness : 2
                        
                        # Debugg
                        print("Label: %s," %label, "Confidence: %f," %confidence)
                        
                        # Draw Rectangle
                        cv2.rectangle(image, (start_x, start_y - label_size[1]),(start_x + label_size[0], start_y + base_line),(255,255,255), cv2.FILLED)
                        # Draw Text
                        cv2.putText(image, label, (start_x, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0)) 
                        
                        # Measure Time and show on Text
                        ai_time = tm.getTimeMilli()
                        # Show AI Processing Time
                        #cv2.putText(image, '{:.2f}(ms)'.format(ai_time), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), thickness=2)
                        
                        '''
                        # Debug show image
                        cv2.imshow(capd_img_list[j],image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        '''
                        
                        # Save AI overlaied image
                        cv2.imwrite(capd_img_list[j],image)
                        
                        # Overlay
                        time.sleep(args['interval']) # Set inteval to repeat do AI
                        # Close Process
                        print('Close AI Process')
                        time.sleep(3)
'''
#def check
a = ai_obj_det(capd_img_list)
print("done")
'''
