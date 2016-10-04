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
from PIL import Image

printer = Printer()
printer.init()

raw_input('Ready?')
printer.capture()
raw_input('Done')

#job = Job('test', Job.get_processor(3))

#gui = Gui()

#instructions = job.process(None)

#gui.setProcessed(Image.new("RGB", (1000, 1000)))

#gui.plot(instructions)
#printer.plotList(instructions)

raw_input('Done')
