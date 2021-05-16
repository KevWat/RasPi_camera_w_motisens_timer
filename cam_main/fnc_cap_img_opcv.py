import cv2
import datetime
path = 'pic/' # Picture Folder Location
def capture_camera(path,width,height):
    capture = cv2.VideoCapture(1) # 0 is camera device number
    ret, frame = capture.read()
    windowsize =(width,height)
    frame = cv2.resize(frame, windowsize)
    cv2.imshow('cap_picture',frame)
    # Save img
    now = datetime.datetime.now()
    filename = path + now.strftime('%Y%m%d_%H%M_%S') + '.jpg'
    output_img = cv2.imwrite(filename,frame)
    # Interlap
    k = cv2.waitKey(1)  # wait 1sec
    capture.release()
    cv2.destroyAllWindows()
    return(filename)
#def check
a = capture_camera(path,800,600)
print(a)
