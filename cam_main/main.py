#!python3.7
# config: UTF-8

import RPi.GPIO as GPIO
import fnc_cap_img_opcv_2camera as cap_opcv # 2 Camera Capture
import fnc_thread_ctrl as thr_ctrl
import fnc_slack_upload as slk_upl # Upload Slack
import fnc_auto_del as at_del # Old file Auto Delete
import fnc_add_ovrl_datetime as ovrl_dt
import fnc_ai_cap as ai_cap
import schedule
from datetime import datetime
import time
import argparse # Set command option "argparse"
import os
import sys

BTN = 21 # GPIO BT Number, GPIO 21
path = 'pic/' # Picture Folder Location

Time = 30*60 # unit seconds

Trigger_Mode = "TimerOn"


################################
# Set & Check Operation Time
################################
# Set Active Time Zone
# e.g. 06:00 - 18:30, Does not compare year & date
# set operation start time
op_start = '6:00'
op_end = '18:30'
time_format = '%H:%M'

def check_time_pri(op_start, op_end, time_format):
        op_st_time_frm = datetime.strptime(op_start, time_format) # Set hour min : YYYY-MM-DD, hh:mm
        op_st_time_frm_hm = datetime.time(op_st_time_frm) # reshape to HH:MM
        op_ed_time_frm = datetime.strptime(op_end, time_format) # Set hour min : YYYY-MM-DD, hh:mm
        op_ed_time_frm_hm = datetime.time(op_ed_time_frm) # reshape to HH:MM
        # Current Time
        current_time = datetime.now().time()
        operation_period = (op_st_time_frm_hm < current_time) & (current_time < op_ed_time_frm_hm)
        print("operation_time:", operation_period)
        return(operation_period)

################################
# Object Start Capture
################################

capd_img_list = []
# start capture
def start_capture():
    if check_time_pri :
        # Camera Capture
        capd_img_list = cap_opcv.capture_camera(path, 640, 480) # Argument(Save Location,Width, Height), return: captured file name
        time.sleep(1)
        print("Timer_capped_Done")
        ## Overlay datetime and Upload each img ##
        for capd_img in capd_img_list:
            # Overlay Date Time
            ovrl_dt.add_ovrl_datetime(capd_img)
            # AI: Object Detection *No return data, just over-write
            ai_cap.ai_obj_det(capd_img_list)
            ## Upload on Slack ##
            slk_upl.slack_upload(capd_img)
            print(capd_img)
            ## Delete Old File ##
            at_del.auto_delete_file(path)
            time.sleep(30) # privent to shoot many pics
            print("Cycle Done")
    else :
        print("Out of Time_priod")

################################
# Object Detect
################################
# Due to Argus BTN exist, need to make this function
def sens_capture(BTN):
    # Sensor Mode Only for Argument
    print("GPIO PIN", BTN)
    start_capture()
    print("Sensor_capped_Done")

# Trigger Selct
if (Trigger_Mode == "TimerOn"):
    print("Timer_mode")
    # unit:sec, Function, False: Paralell / Ture: Single
    thr_ctrl.scheduler(Time, start_capture, False)

if (Trigger_Mode == "SensorOn"):
    print("Sensor_Mode")
    # GPIO Trigger
    GPIO.setmode(GPIO.BCM) #Set BCM number to access GPIO
    GPIO.setup(BTN, GPIO.IN) #BCM No.26pin
    GPIO.add_event_detect(BTN, GPIO.RISING,sens_capture,bouncetime=100)
    print("Sensor_detect")


################################
# Syquence
################################
while True:
    schedule.run_pending()
    time.sleep(1)


try:
    while True:
        #print("No Detect")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.remove_event_detect(BTN)
    GPIO.cleanup()
