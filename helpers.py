import cv2
import math
from termcolor import colored, cprint;

## IMAGES ##
def rotate_cv2_image(mat, angle):
    """Rotate a cv image"""
    height, width = mat.shape[:2]
    image_center = ((width - 1) / 2.0, (height - 1) / 2.0)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)

    # Get Bounding Box
    radians = math.radians(angle)
    sin = abs(math.sin(radians))
    cos = abs(math.cos(radians))
    bound_w = (width * cos) + (height * sin)
    bound_h = (width * sin) + (height * cos)

    # Set Translation
    rotation_mat[0, 2] += ((bound_w - 1) / 2.0 - image_center[0])
    rotation_mat[1, 2] += ((bound_h - 1) / 2.0 - image_center[1])

    rotated_mat = cv2.warpAffine(mat, rotation_mat, (int(bound_w), int(bound_h)))
    return rotated_mat


## PRINT ##
def print_ok(s = ''):
    cprint('[OK] ' + s, 'green', attrs=['bold'])

def print_fail(s = ''):
    cprint('[FAIL] ' + s, 'red', attrs=['bold'])

def print_help():
    cprint('Usage:', attrs=['bold'])
    print '-h --help : show usage'
    print '-l --list : list all jobs'
    print '-n --new {file} : start a new job and print the text from {file}'
    print '-r --resume {job} : resume a job'
