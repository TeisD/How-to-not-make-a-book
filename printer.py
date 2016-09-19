import config
import cv2
import gphoto2 as gp
import helpers
import numpy as np
import os
from PIL import Image
import pyocr
import serial
from serial.tools import list_ports
import subprocess
import sys
import time

print_ok = helpers.print_ok
print_fail = helpers.print_fail

class Printer:
    """Comunicate with the hardware (and OCR library): plotter, camera and OCR"""

    def __init__(self, port = None):
        """Create a new printer

        Keyword arguments:
        port -- optional string to define the serial port (default None). If no port is given, the first port with an Arduino connected will be selected during initialisation."""

        self.port = port
        self.serial = None
        self.context = gp.Context()
        self.camera = gp.Camera()
        self.ocr = None
        self.currentPosition = (0,0)
        self.convert = None
        self.tool = 'PEN';

    def init(self):
        """Initialize the connections to the hardware components and load the OCR library."""
        ## Connect to the plotter
        print("Connecting to plotter...");
        if not config.DEBUGGING:
            try:
                if self.port is None:
                    self.port = serial.tools.list_ports.grep("modemf").next()[0]
                self.serial = serial.Serial(self.port, 115200)
                time.sleep(5) # give some time to the port to open
                self.home()
                print_ok()
            except StopIteration:
                print_fail('Could not find /dev/cu.usbmodemf*. Is the Arduino connected?')
                self.terminate()
            except serial.serialutil.SerialException:
                print_fail('Could not connect to \'' + self.port + '\'.')
                self.terminate()
        else:
            print_ok('(debugging mode)')

        ## Connect to the camera
        print("Connecting to camera...")
        if (not config.DEBUGGING and not config.SKIP_CAMERA):
            try:
                subprocess.call('killall PTPCamera', shell=True)
                self.camera.init(self.context)
                print_ok()
            except gp.GPhoto2Error:
                print_fail('Could not find a supported camera.')
                self.terminate()
        else:
            print_ok('(debugging mode)')

        ## Initialize OCR
        print("Initializing OCR library...")
        try:
            self.ocr = pyocr.get_available_tools()[0] # tools are returned in the recommended order of usage
            print_ok()
            print(self.ocr.get_name() + ' will be used for OCR')
        except IndexError:
            print_fail('No OCR libraries installed.')
            self.terminate()

        ## Calibrate plotter if necessary
        print("Calibrating...")
        try:
            if os.path.isfile(config.CALIBRATION_PATH) and os.path.getsize(config.CALIBRATION_PATH) > 0:
                with open(config.CALIBRATION_PATH) as f:
                    from_pt = [tuple(map(float, i.split(','))) for i in f] #file format is float,float\nfloat,float...
                to_pt = config.CALIBRATON_POINTS
                self.convert = helpers.affine_fit(from_pt, to_pt)
                if(config.DEBUGGING): print self.convert.to_str()
            else:
                self.calibrate()
        except Exception,e:
            print_fail(str(e))
            self.terminate()
        print_ok()

    def capture(self):
        """Capture a page

        number -- An integer representing the current page number
        """
        if not config.DEBUGGING:
            file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE, self.context))
            #print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
            camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, self.context))
            filename = time.strftime('images/%Y%m%d_%H%M%S') + '.jpg'
            gp.check_result(gp.gp_file_save(camera_file, filename))
        else:
            filename = 'debug.jpg'
        im = Image.open(filename).convert('RGB')
        im = im.crop((950, 400, 3200, 2300)) #hardcoded page boundaries. oeps
        # rotate image counter-clockwise if necesary
        if(im.size[0] < im.size[1]):
            im = im.rotate(90, expand=1)
        im.save(filename[:-4]+'_edit.jpg')
        return im

    def calibrate(self):
        helpers.print_title("PRINTER CALIBRATION")
        raw_input('Please put a white page on the plotting surface')
        for c_point in config.CALIBRATON_POINTS:
            self.go(c_point)
            self.circle(2.5)
        # plot circles at some coordinates
        self.home()
        image = self.capture()
        image = cv2.cvtColor( np.array(image), cv2.COLOR_RGB2GRAY );
        image = cv2.medianBlur(image, 5)
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1,250,param1=100,param2=30,minRadius=15,maxRadius=35)
        circles = circles[0,:]

        if len(circles) != len(config.CALIBRATON_POINTS):
            helpers.print_fail('Calibration detected {0} calibration points.'.format(len(circles)))
            self.terminate()

        to_pt = config.CALIBRATON_POINTS # plotter coordinates
        from_pt = []
        f = open(config.CALIBRATION_PATH, 'w') # create new and empty existing
        for i in circles:
            from_pt.append((i[0],i[1]))
        from_pt = sorted(from_pt, key=lambda tup: tup[1]) #sort by growing y (which is x for the plotter)
        for i in from_pt:
            f.write('{0},{1}\n'.format(i[0],i[1]))
        f.close()
        self.convert = helpers.affine_fit(from_pt, to_pt)

    def convertCoordinate(self, c):
        """Convert the image coordinate c to a plotter coordinate
        c -- the coordinate Tuple to convert"""

        point = self.convert.transform(c)

        return (round(point[0], 2), round(point[1], 2))

    def convertDistance(self, c, d):
        """Convert the image distance d near point c to a plotter distance
        d -- the distance Integer to convert
        c -- a coordinate Tuple close to point d"""

        start = self.convert.transform(c)[0]
        end = self.convert.transform((c[0]+d, c[1]+d))[0]
        return abs(round(end - start, 2))

    def plotList(self, instructions):
        """Plot a list of instructions

        instructions -- a list of instructions to plot"""

        for instruction in instructions:
            self.plot(instruction)

    def plot(self, instruction):
        """Plot an instruction.

        instruction -- the instruction to print. Accepted formats are:
            ["line", (x,y), (x,y)]
            ["arc", (center x, center y), radius]
            ["box", (left, bottom), (right, top)]"""

        self.go(self.convertCoordinate(instruction.start))
        if(instruction.type == "line"):
            self.line(self.convertCoordinate(instruction.end))
        elif instruction.type == 'circle':
            self.circle(self.convertDistance(instruction.start, instruction.radius))

    def go(self, c):
        """Go to a point

        c -- the coordinate Tuple to go"""

        self.send('M3') # pen up and laser off
        self.send('G0 X{0} Y{1}'.format(c[0],c[1]))
        self.currentPosition = c
        if config.VERBOSE:
            print('current position: ' + str(self.currentPosition))

    def line(self, c):
        """Draw a line from the current location to c

        c -- the coordinate Tuple to go"""

        self.on()
        self.send('G1 X{0} Y{1}'.format(c[0],c[1]))
        self.off()
        self.currentPosition = c

    def circle(self, r):
        """Draw a circle from the current location with radius c

        r -- an integer describing the radius"""

        self.go((self.currentPosition[0] - r, self.currentPosition[1])) # go to a place on the circle
        self.on()
        self.send('G2 X{0} Y{1} I{2}'.format(self.currentPosition[0], self.currentPosition[1], r)) # make a full circle
        self.off()

    def on(self):
        if(self.tool == 'PEN'):
            self.send('F4000')
            self.send('M4') # pen down
            time.sleep(0.125)
        elif(self.tool == 'LASER'):
            self.send('F350')
            self.send('S1000')

    def off(self):
        if(self.tool == 'PEN'): self.send('M3')
        elif(self.tool == 'LASER'): self.send('S0') #pen up

    def home(self):
        self.send('$H')
        self.currentPosition = (0,0)

    def send(self, c):
        """Send a command to the plotter

        c -- the command String to send"""
        print(c)
        if not config.DEBUGGING:
            self.serial.write(c)
            self.serial.write('\n')
            self.checkResponse()

    def checkResponse(self):
        response = self.serial.readline()[:-2] # strip the newline character
        while response.lower() != 'ok':
            print(response)
            time.sleep(1) # wait one sec before checking again
            response = self.serial.readline()[:-2]
        helpers.print_ok()

    def terminate(self):
        self.camera.exit(self.context)
        sys.exit()

    def setTool(self, tool):
        self.tool = tool

    def getOcr(self):
        return self.ocr
