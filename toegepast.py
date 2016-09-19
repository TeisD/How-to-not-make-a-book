import config
from page import Page
from printer import Printer
from gui import Gui
from job import Job
import helpers

import os, sys, getopt, time

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import threading

def main(argv):
    """Print a book!

    Arguments:
    -h --help -- show usage
    -l --list -- list all jobs
    -c --calibrate -- calibrate the plotter
    -n --new -- start a new job
    -r --resume {job} -- resume a job"""

    job = None

    try:
        opts, args = getopt.getopt(argv[1:],"hlcnr:",["help","list","calibrate","new","resume="])
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
            mode = raw_input("Job mode: ")
            lang = raw_input("Job language (nld/eng): ")
            #job = jobs.Cookbook(name, mode, lang, "test")
            job = Job(name, Job.get_processor(mode), lang)
            break
        elif opt in ("-r", "--resume"):
            print("todo")
            break

    printer = Printer()
    printer.init()
    gui = Gui()

    while True:
        page = Page(printer.capture(), printer.getOcr(), job.getLanguage())
        gui.setOriginal(page.getImageOriginal())
        gui.setProcessed(page.getImageProcessed())
        instructions = job.process(page)
        threading.Thread(gui.plot(instructions))
        threading.Thread(printer.plotList(instructions))
        printer.home()
        raw_input("Please turn the page and press enter to continue...")




if __name__ == "__main__":
    main(sys.argv)
