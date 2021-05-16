import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import cv2
import datetime
path = 'pic/' # Picture Folder Location

#video = [0,2] # put /dev/video
video = [0] # put /dev/video

def capture_camera(path,width,height):
    # Support Multiple Cameras
    #video = [0,3]  # put /dev/video
    pic_list = [] # return picture name
    for i in  video:
        camnum = i
        capture = cv2.VideoCapture(i) # 0 is camera device number
        ret, frame = capture.read()
        if ret == True:
            print("Frame exist")
        if ret == False:
            print("Frame empty")
            break
        windowsize =(width,height)
        frame = cv2.resize(frame, windowsize)
        cv2.imshow('cap_picture',frame)
        # Save img
        now = datetime.datetime.now()
        filename = path + now.strftime('%Y%m%d_%H%M_%S')+'_cam'+str(camnum)+'.jpg'
        output_img = cv2.imwrite(filename,frame)
        pic_list.append(filename)
        # Interlap
        k = cv2.waitKey(1)  # wait 1sec
        capture.release()
        cv2.destroyAllWindows()
    print(pic_list)
    return(pic_list)

#def check
#a = capture_camera(path,800,600)
#print(a)


