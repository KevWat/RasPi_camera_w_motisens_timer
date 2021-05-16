import datetime
import PIL
from PIL import Image
from PIL import ExifTags
import cv2 as cv

# Overlay Text
# Time (Option: Date, Year)  

def add_ovrl_datetime(file_path_name):
 # Date Time
 now = datetime.datetime.now()
 # Overlay
 img = cv.imread(file_path_name)
 cv.putText(
    img, # cv.imread  image object
    #'2020/12/18', # charactor
    now.strftime('%H:%M'), # Time
    #(530, 460), # Bottom Right Pixel Position of Text
    (10, 30), # Top Left Pixel Position of Text
    cv.FONT_HERSHEY_PLAIN, # Font Style,CV_FONT_HERSHEY_PLAIN,CV_FONT_HERSHEY_SCRIPT_SIMPLEX and so on
    2, # Font Size
    (255, 255, 255), # Font Color
    1, # Font Thickness
    cv.LINE_AA) # 4,8,cv.LINE_AA have to be selected
 cv.imwrite(file_path_name, img)

'''
a = add_ovrl_datetime('pic/sample.jpg')
print('done')
'''
