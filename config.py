DEBUGGING = 0; # test-runs without camera and plotter connected and shows aditional messages during runtime
DEBUGGING_IMAGE = 'images/20161009_170522.jpg' # filename of the image to use for capture in debuggin mode
SKIP_CAMERA = 0 # don't connect to the camera, even when debugging mode is false
VERBOSE = 1; # show verbose output while plotting

LASER_RES = 0.5; # resolution of the laser when creating a fill from scanlines in mm.
MARGIN = 5 # the margin for outlines in px (on the image)

CALIBRATON_POINTS = [(40,50), (50,250), (150,150), (240,50), (250,250)] # Array of 4 calibration points (in plotter coordinate space, increasing on x-axis)
CALIBRATION_PATH = 'calibration.conf' # Path to a file which holds the calibration points (in image coordinate space)

ROTATION = 180 #the orientation of the camera in degrees
GUI_SCALE = 0.2 #the amount to scale images displayed with opencv's imshow method
