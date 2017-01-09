from page import Page
from gui import Gui
from job import Job
from printer import Printer
import processor
import helpers
import gphoto2 as gp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from PIL import Image

printer = Printer()
printer.init()
printer.capture()

sys.exit()

raw_input('Arc test')
instructions = []
radius = 25
center = (1000,2000)
quadrant = 1
instructions.append(processor.Arc(center,radius,0))

while(radius <= 200):
    instructions.append(processor.Arc(center, radius, quadrant))
    radius += (quadrant%2)*25
    center = (center[0], center[1] + (quadrant%2)*25)
    if(quadrant == 1): center = (center[0], center[1] - 50)
    quadrant += 1
    if(quadrant > 3): quadrant = 0

printer.plotList(instructions)


raw_input('Laser test')
printer.tool='PEN'
while(True):
    printer.go((20,10))
    printer.on()
    printer.line((200, 10))
    printer.line((200,50))
    printer.line((20, 50))
    printer.line((200, 50))
    printer.line((200,100))
    printer.line((20,100))
    printer.line((20,150))
    printer.line((200, 150))
    printer.line((200, 200))
    printer.line((20,200))
    printer.line((20, 250))
    printer.line((200,250))
    printer.off()
#printer.capture()
raw_input('Done')



gui = Gui()
gui.setProcessed(Image.new("RGB", (1000, 1000)))

gui.plot(instructions)


#job = Job('test', Job.get_processor(3))

#gui = Gui()

#instructions = job.process(None)

#gui.setProcessed(Image.new("RGB", (1000, 1000)))

#gui.plot(instructions)
#printer.plotList(instructions)

raw_input('Done')
