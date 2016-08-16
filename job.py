import cv2
import numpy as np;
from PIL import Image

class Job:
    """A print job consists out of a text to print and a book to be reprinted"""

    def __init__(self, txt = None, currentPage = 1):
        """Create a new page

        Keyword arguments:
        txt -- The text to be printed
        currentPage -- The current page of the job"""

        self.txt = txt
        self.currentPage = currentPage
