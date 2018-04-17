import numpy as np
import argparse
import cv2
import time


#cap = cv2.VideoCapture(0) # for video
#Set Width and Height 
#cap.set(3,1280)
#cap.set(4,720)

# X and Y coordinates of the drone
x = 0.545547
y = -0.87374

# Distance from the drone to the hoop
R = ((x**2) + (y**2))**0.5

# Height of the drone
z = 1

# The above step is to set the Resolution of the Video. The default is 640x480.
# This example works with a Resolution of 640x480.

#img = cv2.imread("C:\\Users\\Dell\\Desktop\\lab3\\images\\12.jpeg")
#img2 = cv2.imread("C:\\Users\\Dell\\Desktop\\lab3\\images\\90.PNG")
img = cv2.imread("C:\\Users\\Dell\\Desktop\\lab3\\lab_4\\5.jpeg")
cv2.imshow('ss', img)
while (True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    

    # load the image, clone it for output, and then convert it to grayscale
    img2 = img.copy()

    #convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #define boundaries
    lower_blue = np.array([86,31,4])
    upper_blue = np.array([235,206,135])

    #mask the image
    mask = cv2.inRange(img, lower_blue, upper_blue)

    #for viewing the masked image
    res = cv2.bitwise_and(img,img, mask = mask)
    #cv2.imshow ('masked image', res)

    #Adaptive tresholding
    gray = cv2.adaptiveThreshold(mask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,3.5)

    #for cleaning
    kernel = np.ones((1,2),np.uint8)
    gray = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = 2)
    
    #Apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise.
    gray = cv2.GaussianBlur(gray,(5,5),0)
    gray = cv2.medianBlur(gray,5)

    cv2.imshow ('masked image', gray)
    # detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 500, param1=100, param2=75, minRadius=0, maxRadius=0)
    
    

    
    #Technically we do not need the rest of the code, uncomment to see the detection

    #ensure at least some circles were found
    if circles is not None:
        
        #convert the (x,y) coordinates and radius of the circle to intigers
        circles = np.round(circles[0, :]).astype("int")

        #loop over coordinates and circle radius
        for (x,y,r) in circles:
            ba = x
            print (ba)
            #draw circles in the output image and a rectangle on the center
            cv2.circle(img2, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(img2, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            
            #time.sleep(0.5)
            print (x,y,r)

            #display
            #cv2.imshow('gray', gray)
            cv2.imshow('frame', img2)

            #to find position
            x_rel = (x-320)*2.7/640
            y_rel = (180-y)*2.7/640
            print (x_rel, y_rel)

            
    break

# Calculating the height of the drone
Az = z + (((180 - y)*(R*np.sin(29.36)))/360)
print(Az)
