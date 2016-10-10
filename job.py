import config
import cv2
from collections import namedtuple
import helpers
import json
import numpy as np
from PIL import Image
import processor
from termcolor import colored, cprint;

class Job:
    """A print job consists out of a text to print and a book to be reprinted"""

    @staticmethod
    def get_processor(mode):
        if int(mode) == 1: return processor.Processor()
        elif int(mode) == 2: return processor.Circle()
        elif int(mode) == 3: return processor.Cookbook()
        elif int(mode) == 4: return processor.Instructions()

    def __init__(self, name, processor, lang = 'nld'):
        """Create a new job

        Keyword arguments:
        name -- The name of the job
        path -- The processor to use with every the page
        lang -- The language of the job"""

        self.name = name
        self.processor = processor
        self.lang = lang

        ## Todo: create a file to keep the progress (json? see http://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file)

    def init(self, page):
        self.processor.init(page)

        properties = {
            'name': self.name,
            'lang': self.lang,
            'processor': self.processor.mode,
            'processor_properties': self.processor.get_properties()
        }

        return properties

    def process(self, page):
        return self.processor.process(page)
        """Processes a page by reading the file character by character and matching the OCR text until the end of the page is finished
        Current implementations breaks (keeps searching) on special characters

        Keyword arguments:
        page -- the Page object to process"""

    def get_name(self):
        return self.name

    def get_language(self):
        return self.lang
