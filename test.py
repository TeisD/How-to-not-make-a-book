from page import Page
from printer import Printer
import gphoto2 as gp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

printer = Printer()
printer.init()
page = Page(printer.capture(1), printer.ocr, 'eng')

plt.figure(figsize=(20,10))
plt.subplot(121)
plt.imshow(page.getImageOriginal())
plt.subplot(122)
plt.imshow(page.getImageProcessed())
plt.show()
