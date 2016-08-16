import cv2
import numpy as np;
from PIL import Image

class Page:
    """Process a captured image (clean up & do OCR)"""

    def __init__(self, image, ocr, lang):
        """Create a new page

        Keyword arguments:
        imageOriginal -- A PIL image containing text
        imageProcessed -- A cleaned and processed PIL image
        ocr -- a pyocr instance
        lang -- A 3-letter string defining the language of the page"""

        self.imageOriginal = image
        self.imageProcessed = None
        self.ocr = ocr
        self.lang = lang

    def getImageOriginal(self):
        return self.imageOriginal

    def getImageProcessed(self):
        if self.imageProcessed is None:
            self.process()
        return self.imageProcessed

    def clean(self, image):
        ret,image = cv2.threshold(image,152,255,cv2.THRESH_BINARY)
        return image

    def process(self):
        # convert from PIL to grayscale cv2
        image_cv = cv2.cvtColor(np.array(self.imageOriginal), cv2.COLOR_RGB2GRAY)
        # clean
        image_cv = self.clean(image_cv)
        # convert back to PIL
        self.imageProcessed = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_GRAY2RGB))
        # do OCR
        #angle = self.ocr.detect_orientation(self.imageProcessed, self.lang)
        #print("Rotation: " + str(angle))
        #image = image.rotate(angle['angle'], expand=1)
        #txt = ocr.image_to_string(
        #    image,
         #   lang,
        #    builder=pyocr.builders.WordBoxBuilder() # returns an array of "word left top right bottom"
        #)

    def show(self):
        self.imageOriginal.show()
