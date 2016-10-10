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
import pickle
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
            name = arg
            if(os.path.isfile('jobs/'+name+'.conf')):
                i = raw_input("Job already exists. Overwrite [Y/N]? ")
                if i.lower() != 'y': sys.exit()
            helpers.print_modes()
            #mode = raw_input("Job mode: ")
            mode = 3
            #lang = raw_input("Job language (nld/eng): ")
            lang = 'eng'
            printer = Printer()
            printer.safe = True
            printer.init()
            job = Job(name, Job.get_processor(mode), lang)
            page = Page(printer.capture(), printer.getOcr(), job.get_language())
            properties = job.init(page)
            with open('jobs/' + name + '.conf', 'wb') as f:
                pickle.dump(properties, f, pickle.HIGHEST_PROTOCOL)
            break
        elif opt in ("-r", "--resume"):
            if(os.path.isfile('jobs/' + arg + '.conf')):
                with open('jobs/' + arg + '.conf', 'rb') as f:
                    p = pickle.load(f)
                    printer = Printer()
                    printer.safe = True
                    printer.init()
                    job = Job(p['name'], Job.get_processor(p['processor']), p['lang'])
                    job.processor.set_properties(p['processor_properties'])
            else:
                helpers.print_fail("Job does not exist.")
                sys.exit()
            break

    #gui = Gui()

    while True:
        page = Page(printer.capture(), printer.getOcr(), job.get_language())
        #gui.setOriginal(page.getImageOriginal())
        instructions = job.process(page)
        #gui.setProcessed(page.getImageProcessed())
        #gui.plot(instructions)
        printer.go((0, 200))
        printer.plotList(instructions)
        printer.home()
        i = raw_input("Please turn the page and press ENTER to continue or Q to quit... ")
        if i == 'q': break

    sys.exit()

if __name__ == "__main__":
    main(sys.argv)
