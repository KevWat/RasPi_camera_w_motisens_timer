#!python3.7
# config: UTF-8

import os
import time

################################
# Delete Old Files
################################
## Delete old file by time stamp
## Delete files as bellow location "pic/"

#path: 'pic/' #Folder Location from Top file
def auto_delete_file(path):
    dir_lst = os.listdir(path)
    print(dir_lst)
    for file_name in dir_lst:
        cr_time = os.path.getatime(path + file_name) #Last access
        cur_time = time.time() # Current Time
        #delta = 60 # 1 min
        #delta = 60*60 # 1 hour
        delta = 60*60*24 # 1 day
        #delta = 60*60*24*7 # 1 week
        if (cur_time - cr_time > delta ): # Current Time - Creamte Time
            os.remove(path + file_name)
            print("Deleted",file_name)
        else :
            print("No Deleted")
