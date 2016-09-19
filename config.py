DEBUGGING = 1; # test-runs without camera and plotter connected and shows aditional messages during runtime
SKIP_CAMERA = 0 # don't connect to the camera, even when debugging mode is false
VERBOSE = 1; # show verbose output while plotting

LASER_RES = 0.5; # resolution of the laser when creating a fill from scanlines in mm.
MARGIN = 5 # the margin for outlines in px (on the image)

CALIBRATON_POINTS = [(40,50), (50,250), (150,150), (240,50), (250,250)] # Array of 4 calibration points (in plotter coordinate space, increasing on x-axis)
CALIBRATION_PATH = 'calibration.txt' # Path to a file which holds the calibration points (in image coordinate space)
