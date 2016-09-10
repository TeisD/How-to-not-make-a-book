import config
from page import Page
from printer import Printer
from job import Job
from gui import Gui
import helpers

import os, sys, getopt, time

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def main(argv):
    """Print a book!

    Arguments:
    -h --help -- show usage
    -l --list -- list all jobs
    -c --calibrate -- calibrate the plotter
    -n --new {file} -- start a new job and print the text from {file}
    -r --resume {job} -- resume a job"""

    job = None

    try:
        opts, args = getopt.getopt(argv[1:],"hlcn:r:",["help","list","calibrate","new=","resume="])
        if not opts:
            raise getopt.GetoptError('No arguments given')
    except getopt.GetoptError:
        helpers.print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            helpers.print_help()
            sys.exit()
        elif opt in('-l', '--list'):
            print('todo')
            sys.exit()
        elif opt in('-c', '--calibrate'):
            if(os.path.isfile(config.CALIBRATION_PATH)):
                os.rename(config.CALIBRATION_PATH, config.CALIBRATION_PATH[:-4]+'_'+time.strftime('%Y%m%d_%H%M%S')+'.txt')
            printer = Printer()
            printer.init()
            sys.exit()
        elif opt in ("-n", "--new"):
            name = raw_input("Job name: ")
            helpers.print_modes()
            mode = None
            while mode != None
                mode = Job.Mode.get(raw_input("Job mode: "))
            job = Job(name, Job.Mode.H_CHAR, arg, 'eng')
            break
        elif opt in ("-r", "--resume"):
            print(todo)
            break

    printer = Printer()
    printer.init()
    gui = Gui()

    while True:
        page = Page(printer.capture(), printer.getOcr(), job.getLanguage())
        gui.setOriginal(page.getImageOriginal())
        gui.setProcessed(page.getImageProcessed())
        matches = job.process(page)
        gui.plot(matches)
        printer.plotList(matches)
        printer.home()
        raw_input("Please turn the page and press enter to continue...")




if __name__ == "__main__":
    main(sys.argv)
