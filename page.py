import cv2

class Page:
    """Process a captured image (clean up & do OCR)"""

    def __init__(self, image):
        """Create a new page

        Keyword arguments:
        image -- A cv2 image"""

        self.image_original = image

    def show(self):
        cv2.imshow("image", self.image_original)
