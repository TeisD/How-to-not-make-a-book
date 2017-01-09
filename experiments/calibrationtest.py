import cv2
import numpy as np

GUI_SCALE = 0.2

#detect circles
image = cv2.imread('calibrationtest.jpg')
image = cv2.cvtColor( np.array(image), cv2.COLOR_RGB2GRAY )
image = cv2.medianBlur(image, 5)
#circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1,250,param1=200,param2=30,minRadius=20,maxRadius=30) #marker
#circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1,250,param1=100,param2=35,minRadius=15,maxRadius=30) #good for blue permanent fineliner
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1,250,param1=60,param2=35,minRadius=15,maxRadius=30)
circles = circles[0,:]

#scale and show
image = cv2.resize(image, (0,0), fx=GUI_SCALE, fy=GUI_SCALE)

for circle in circles:
    cv2.circle(image, (int(circle[0]*GUI_SCALE), int(circle[1]*GUI_SCALE)), 5, (255,255,0))

cv2.namedWindow("test")
cv2.imshow("test", image)

while True:
    # display the image and wait for a keypress
    key = cv2.waitKey(1) & 0xFF
    # escape or space
    if key == 27 or key == 32:
        break

cv2.destroyWindow("test")
