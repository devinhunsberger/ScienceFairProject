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
    #Creates a display that can then be transformed called vid.
    ret, vid = cap.read()
    #This code actually places our TargetPosition1 image ontop of our live video feed.
    dst = cv2.addWeighted(img1, alpha, vid, beta, 0)
    #roi stands for region of interest, or the area we want to scan for the block. 
    roi = vid[230:925, 650:1270]
    #Blurring helps reduce image "noise", light particularly makes it difficult for the scanning process and blurring can partially reduce that. 
    mask = cv2.blur(vid,(1,9))
    #This converts the BGR (in OpenCV it's not RGB but BGR) to grayscale which also helps reduce noise and in general makes it easier to filter and search for a certain color or object. 
    mask = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    #Creates 2 variables we use later for the filtering.
    lower_block = (25, 125, 205)#We know 25,70,75
    upper_block = (32, 255, 255)# and 49,255,255 works
    
    #Creates a display called mask that filters out colors anything out of the lower_block and upper_block parameters within the ROI
    mask = cv2.inRange(roi, lower_block, upper_block)

    #The findContours will find the contours needed to be drawn around the block.     
    ret, thresh = cv2.threshold(mask, 127,255,0)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    
    #This line draws the contours to the main screen.
    final = cv2.drawContours(dst, contours, -1,(0,255,0), 3, 4, hierarchy, 2, (650,225))

    #This chunk of code displays the live feed to a window.
    cv2.imshow('final', final)
    cv2.imshow('mask', mask)
    
    k = cv2.waitKey(27) & 0xFF  #This code checks if the escape key has been pressed to end the camera processes and scanning process.
    if k == 27:
        break
#These processes run after you end the detection process.
cv2.destroyAllWindows()
cap.release()
print(str(process.memory_info().rss) + ' is the number of bytes used in this program!')

#I plan to add more onto the code by the science fair so that it has extra features that don't really pertain to the write up. Such as a frame tracker to see if the processes actually run faster and use less memory than other forms of object detection. 

