from page import Page
from gui import Gui
from job import Job
from printer import Printer
import helpers
import gphoto2 as gp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

#printer = Printer()
#printer.init()

#plt.figure(figsize=(20,10))
#plt.subplot(121)
#plt.imshow(page.getImageOriginal())
#plt.subplot(122)
#plt.imshow(page.getImageProcessed())
#plt.show()

#job = Job('test', Job.Mode.H_CHAR, 'test.txt', 'nld')
#page = Page(printer.capture(), printer.getOcr(), job.getLanguage())

#gui = Gui()

#gui.setOriginal(page.getImageOriginal())
#gui.setProcessed(page.getImageProcessed())
#gui.plot(job.process(page))

#from_pt = ((1,1),(1,2),(2,1),(2,2),(3,3))
#to_pt = ((1,1),(1,4),(4,1),(4,4),(3,3))
#t = helpers.affine_fit(from_pt, to_pt)
#print(t.to_str())
#print(t.transform((1,2)))

#from_pt = [(1,1),(1,2),(2,1),(2,2)]
#to_pt = [(1,1),(1,4),(4,1),(4,4)]
#t = helpers.create_perspective_transform(from_pt, to_pt)
#print(t((4,4)))

img = cv2.imread('images/20160821_180701.jpg');
img = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY );
img = cv2.medianBlur(img, 5)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,250,param1=100,param2=30,minRadius=15,maxRadius=35)
#circles = np.uint16(np.around(circles))

img = cv2.cvtColor( img, cv2.COLOR_GRAY2BGR );

for i in circles[0,:]:
    print(i)
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)

cv2.imshow('detected circles',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

raw_input("Done!")
