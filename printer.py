import config
import cv2
import gphoto2 as gp
import helpers
import pyocr
import serial
from serial.tools import list_ports
import subprocess
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

    def init(self):
        """Initialize the connections to the hardware components and load the OCR library."""
        ## Connect to the plotter
        print("Connecting to plotter...");
        if not config.DEBUGGING:
            try:
                if self.port is None:
                    self.port = serial.tools.list_ports.grep("modemf").next()[0]
                self.serial = serial.Serial(self.port, 115200)
                time.sleep(1) # give some time to the port to open
                print_ok()
            except StopIteration:
                print_fail('Could not find /dev/cu.usbmodemf*. Is the Arduino connected?')
            except serial.serialutil.SerialException:
                print_fail('Could not connect to \'' + self.port + '\'.')
        else:
            print_ok('(debugging mode)')

        ## Connect to the camera
        print("Connecting to camera...")
        if not config.DEBUGGING:
            try:
                subprocess.call('killall PTPCamera', shell=True)
                self.camera.init(self.context)
                print_ok()
            except gp.GPhoto2Error:
                print_fail('Could not find a supported camera.')
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

    def capture(self):
        file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE, self.context))
        #print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, self.context))
        filename = time.strftime('%Y%m%d_%H%M%S') + '.jpg'
        gp.check_result(gp.gp_file_save(camera_file, filename))
        return cv2.imread(filename)
