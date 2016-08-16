from page import Page
from printer import Printer
from job import Job
import helpers

import sys, getopt

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def main(argv):
    """Print a book!

    Arguments:
    -h --help -- show usage
    -l --list -- list all jobs
    -n --new {file} -- start a new job and print the text from {file}
    -r --resume {job} -- resume a job"""

    job = None

    try:
        opts, args = getopt.getopt(argv[1:],"hln:r:",["help","list","new=","resume="])
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
        elif opt in ("-n", "--new"):
            job = Job(arg)
            # naam voor de job ingeven!
            break
        elif opt in ("-r", "--resume"):
            print(todo)
            break

    printer = Printer()
    printer.init()



if __name__ == "__main__":
    main(sys.argv)
