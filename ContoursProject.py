import cv2
import numpy as np
import psutil
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
img1 = cv2.imread(r'C:\Users\BriterDayz\Desktop\SCIENCEFAIR\TargetPosition1.png')
alpha = 0.7
beta = 0.7
kernel = np.ones((3,3))
process = psutil.Process(os.getpid())
while True:
    ret, vid = cap.read()
    dst = cv2.addWeighted(img1, alpha, vid, beta, 0)
    roi = vid[230:925, 650:1270]
    mask = cv2.blur(vid,(1,9))
    mask = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_block = (25, 125, 205)#We know 25,70,75
    upper_block = (32, 255, 255)# and 49,255,255 works

    mask = cv2.inRange(roi, lower_block, upper_block)

    ret, thresh = cv2.threshold(mask, 127,255,0)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    final = cv2.drawContours(dst, contours, -1,(0,255,0), 3, 4, hierarchy, 2, (650,225))
    cv2.imshow('final', final)
    cv2.imshow('mask', mask)
    
    k = cv2.waitKey(27) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()
print(str(process.memory_info().rss) + ' is the number of bytes used in this program!')

