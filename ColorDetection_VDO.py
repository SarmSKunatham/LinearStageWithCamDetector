import cv2
import numpy as np


# img = cv2.imread('HSV.jpg')
# frameHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# hueLow = 20
# satLow = 200
# valLow = 200
# hueHigh = 30
# satHigh = 300
# valHigh = 300
# lowerBound=np.array([hueLow,satLow,valLow])
# upperBound=np.array([hueHigh,satHigh,valHigh])
# myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
# cv2.imwrite('Mymask.jpg', myMask)

cam = cv2.VideoCapture(0) # Open the camera named "cam" for video capturing

while True:
    retval, img = cam.read() # Read the image for the camera
    # img = img[:,:] # Cropping
    # grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # Convert to gray color
    # ret,thresh = cv2.threshold(frameHSV,127,255,cv2.THRESH_BINARY) # Threshold
    frameHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hueLow = 10
    satLow = 150
    valLow = 150
    hueHigh = 120
    satHigh = 400
    valHigh = 400
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV, lowerBound, upperBound)
    orange=cv2.bitwise_and(img,img,mask=myMask)
    contours, hierarchy = cv2.findContours(myMask, 1, 2)
    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frameHSV, (cX, cY), 7, (255, 255, 255), -1)
        print((cX,cY))
        
    # height, width, _ = orange.shape
    # min_x, min_y = 0, 0
    # max_x = max_y = 0
    # print(contours)
    # if contours != ():
    #     for contour, hier in zip(contours, hierarchy):
    #         (x,y,w,h) = cv2.boundingRect(contour)
    #         min_x, max_x = min(x, min_x), max(x+w, max_x)
    #         min_y, max_y = min(y, min_y), max(y+h, max_y)
    #         cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 2)
    # if contours != (): # Check that the contour exist
    #     cnt = contours[0] # Obtain array of contour points
    #     (x,y),radius = cv2.minEnclosingCircle(cnt)
    #     center = (int(x),int(y))
    #     radius = int(radius)
    #     cv2.circle(img,center,radius,(0,255,0),2) # Plot the enclosing circle
    cv2.imshow('Object Detection',img)
    # contours, hierarchy = cv2.findContours(thresh, 1, 2)
    # if contours != (): # Check that the contour exist
    #     cnt = contours[0] # Obtain array of contour points
    #     (x,y),radius = cv2.minEnclosingCircle(cnt)
    #     center = (int(x),int(y))
    #     radius = int(radius)
    #     cv2.circle(img,center,radius,(0,255,0),2) # Plot the enclosing circle
    # cv2.imshow('Object Detection',img) # Display the image
    cv2.imshow('HSV Object Detection',frameHSV)
    cv2.imshow('HSV Object Detection',orange)

    if cv2.waitKey(1) != -1: # Wait for 1 ms, check if any key is pressed
        # cv2.imwrite('HSV.jpg',frameHSV)
        break

cam.release() # Close the camera
cv2.destroyAllWindows() # Close the image window