# TEST CALIBRATION

from printer import Printer
from page import Page
import matplotlib.pyplot as plt
import os
import config
import time
import helpers
from PIL import Image

if(os.path.isfile(config.CALIBRATION_PATH)):
    os.rename(config.CALIBRATION_PATH, config.CALIBRATION_PATH[:-4]+'_'+time.strftime('%Y%m%d_%H%M%S')+'.txt')
printer = Printer()
printer.init()

page = printer.capture()

ax = plt.gca()
fig = plt.gcf()
implot = ax.imshow(page)

def onclick(event):
    print('button=%d, x_img=%f, y_img=%f, x_plot=%f, y_plot=%f' %
          (event.button, event.xdata, event.ydata, printer.convert.transform((event.xdata, event.ydata))[0], printer.convert.transform((event.xdata, event.ydata))[1]))
    printer.line(printer.convert.transform((event.xdata, event.ydata)))

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

printer.home()
