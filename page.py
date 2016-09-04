import config
import cv2
import pyocr, pyocr.builders
import numpy as np;
from PIL import Image

class Page:
    """Process a captured image (clean up & do OCR)"""

    def __init__(self, image, ocr, lang = 'eng'):
        """Create a new page

        Keyword arguments:
        imageOriginal -- A PIL image containing text
        imageProcessed -- A cleaned PIL image
        ocr -- a pyocr instance
        lang -- A 3-letter string defining the language of the page"""

        self.imageOriginal = image
        self.imageProcessed = None
        self.ocr = ocr
        self.lang = lang
        self.characters = None
        self.words = None

    def getImageOriginal(self):
        return self.imageOriginal

    def getImageProcessed(self):
        if self.imageProcessed is None:
            self.process()
        return self.imageProcessed

    def getCharacters(self):
        if self.characters is None:
            self.characters = self.performOcr(pyocr.tesseract.CharBoxBuilder())
        return self.characters

    def getWords(self):
        if self.characters is None:
            self.characters = self.performOcr(pyocr.builders.WordBoxBuilder())
        return self.characters

    def performOcr(self, builder):
        """ Perform Optical Character Recognition and return the array of characters, words or lines

        Keyword arguments:
        builder -- The PyOCR builder to be used for processing"""

        if config.DEBUGGING:
            print("Performing OCR...")
        ret = self.ocr.image_to_string(self.getImageProcessed(), self.lang, builder = builder)
        if config.DEBUGGING:
            print("OCR done!")
        return ret

    def process(self):
        """ Prepare the image for OCR."""
        # convert from PIL to grayscale cv2
        image_cv = cv2.cvtColor(np.array(self.imageOriginal), cv2.COLOR_RGB2GRAY)
        # clean
        ret,image_cv = cv2.threshold(image_cv,152,255,cv2.THRESH_BINARY)
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
