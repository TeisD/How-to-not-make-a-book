import json
import numpy as np
import cv2
import config
import sys
import cookbook
import random
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Instruction(object):

    def __init__(self, type, start, cont = False):
        self.type = type
        self.start = start
        self.continuous = cont

class Line(Instruction):

    def __init__(self, start, end, cont = False):
        self.type = "line"
        self.start = start
        self.end = end
        self.continuous = cont

class Circle(Instruction):

    def __init__(self, start, radius, cont = False):
        self.type = "circle"
        self.start = start
        self.radius = radius
        self.continuous = cont

class Rect(Instruction):

    def __init__(self, start, end, cont = False):
        self.type = "rect"
        self.start = start
        self.end = end
        self.continuous = cont

class Box:

    def __init__(self, box, is_character=False):
        if is_character:
            self.box = box
        else:
            self.box = str(box).split(' ')
        self.left = int(self.box[1])
        self.bottom =  int(self.box[2])
        self.right = int(self.box[3])
        self.top = int(self.box[4])

    def match(self, needle):
        pass

    def get(self):
        return self.box

    def getText(self):
        return str(self.box[0])

    def getStart(self):
        return (self.getLeft(), self.getTop())

    def getEnd(self):
        return (self.getRight(), self.getBottom())

    def getBox(self):
        return [self.getStart(), self.getEnd()]

    def getLeft(self):
        return self.left

    def getBottom(self):
        return self.bottom

    def getRight(self):
        return self.right

    def getTop(self):
        return self.top

    def getHeight(self):
        return self.getTop() - self.getBottom()

    def getWidth(self):
        return self.getRight() - self.getLeft()

    def getMiddle(self):
        return int(self.getBottom() + self.getHeight()/2)

    def setLeft(self, left):
        self.left = left

    def setBottom(self, bottom):
        self.bottom = bottom

    def setRight(self, right):
        self.right = right

    def setTop(self, top):
        self.top = top

    def stroke(self):
        return None

    def strike(self):
        return Line((self.getLeft(), self.getMiddle()), (self.getRight(), self.getMiddle()))

class Character(Box):

    def match(self, needle):
        #todo: uitbreiden naar een functie die accentjes toevoegt op karakters
        if self.getText().lower() == needle.lower():
            return True
        else:
            return False

""" More on Hershey font: http://ghostscript.com/doc/current/Hershey.htm """
class Font(object):

    OFFSET_SPECIAL = 700
    OFFSET_CAPITALS = 500
    OFFSET_SMALL = 600
    LINEHEIGHT = 40
    BASELINE = 9
    SPACE = 10

    def __init__(self, scale = 1):
        with open('fonts/hershey-occidental.json') as data_file:
            self.font = json.load(data_file)
        self.scale = scale
        self.start = (0, 0)
        self.box = None
        self.current = (self.start[0], self.start[1] + self.scale*Font.BASELINE)

    def set_scale(self, scale):
        self.scale = scale

    """Set a start position for the text

    start = (top, left)"""
    def set_start(self, start):
        self.start = start
        self.current = (self.start[0], self.start[1] + self.scale*Font.BASELINE)
    def get_start(self):
        return self.start

    """Set a bounding box for the text

    box = (width, height)"""
    def set_box(self, box):
        self.box = box
    def get_box(self):
        return self.box

    def phrase(self, p):
        instructions = []
        p = p.split()
        for w in p:
            #word
            if self.box is not None: #check if it fits
                bbox = self.get_word_box(w)
                if(self.current[0] + bbox[0] > self.start[0] + self.box[0]): #too large? move to new line
                    self.current = (self.start[0], self.current[1] + self.scale* Font.LINEHEIGHT)
                    if(self.current[1] - Font.LINEHEIGHT > self.start[1] + self.box[1]): #too large? stop
                        return []# don't draw anything
            for l in w:
                instructions += self.letter(l)
            #whitespace
            self.current = (self.current[0] + self.scale * Font.SPACE, self.current[1])
        return instructions

    def letter(self, l):
        glyph = self.glyph(self.map(l))

        if glyph is None:
            self.current = (self.current[0] + self.scale * Font.SPACE, self.current[1])
            return []

        instructions = []
        self.current = (self.current[0] - self.scale * glyph['left'], self.current[1])
        for line in glyph["lines"]:
            prev_end = self.current
            for i in range(0, len(line)-1):
                start = tuple(np.add(self.current, tuple(self.scale*x for x in tuple(line[i]))))
                cont = (start == prev_end)
                end = tuple(np.add(self.current, tuple(self.scale*x for x in tuple(line[i+1]))))
                prev_end = end
                instructions.append(Line(start, end, cont))
        self.current = (self.current[0] + self.scale * glyph['right'], self.current[1])
        return instructions

    """return the dimensions of the word w

    returns (width, height)"""
    def get_word_box(self, w):
        width = 0
        height = 0
        for l in w:
            glyph = self.glyph(self.map(l))
            if glyph is not None:
                width += glyph["right"] - glyph["left"] # right - left
                height = max(height, glyph["bbox"][1][1] - glyph["bbox"][0][1]) # top - bottom
        return (self.scale*width, self.scale*height)

    """returns the dimensions of the sentence p
    currently returns THE WRONG width"""
    def get_size(self, p):
        p = p.split()
        width = 0
        height = 0
        current = self.current
        for w in p:
            #word
            if self.box is not None: #check if it fits
                bbox = self.get_word_box(w)
                if height < bbox[1]: height = bbox[1]
                if(current[0] + bbox[0] > self.box[0]): #too large? move to new line
                    current = (self.start[0], current[1] + Font.LINEHEIGHT)
            #whitespace
            current = (current[0] + self.scale * Font.SPACE, current[1])
        return (width, height)


    """ return a character from a HERSHEY character code """
    def glyph(self,c):
        for glyph in self.font:
            if glyph['charcode'] == c: return glyph

    """ map an ASCII character code to HERSHEY """
    def map(self,c):
        if (ord(c) < 33): return #unused
        if (ord(c) == 33): return Font.OFFSET_SPECIAL + 14 #!
        if (ord(c) == 34): return Font.OFFSET_SPECIAL + 17 #"
        if (ord(c) == 35): return Font.OFFSET_SPECIAL + 33 ##
        if (ord(c) == 36): return Font.OFFSET_SPECIAL + 19 #$
        if (ord(c) == 37): return #%
        if (ord(c) == 38): return Font.OFFSET_SPECIAL + 34 #&
        if (ord(c) == 39): return Font.OFFSET_SPECIAL + 16 #'
        if (ord(c) == 40): return Font.OFFSET_SPECIAL + 21 #(
        if (ord(c) == 41): return Font.OFFSET_SPECIAL + 22 #)
        if (ord(c) == 42): return Font.OFFSET_SPECIAL + 28 #*
        if (ord(c) == 43): return Font.OFFSET_SPECIAL + 25 #+
        if (ord(c) == 44): return Font.OFFSET_SPECIAL + 11 #,
        if (ord(c) == 45): return Font.OFFSET_SPECIAL + 24 #-
        if (ord(c) == 46): return Font.OFFSET_SPECIAL + 10 #.
        if (ord(c) == 47): return Font.OFFSET_SPECIAL + 20 #/
        if (ord(c) > 47 and ord(c) < 58): return Font.OFFSET_SPECIAL + (ord(c) - 48) #numbers
        if (ord(c) == 58): return Font.OFFSET_SPECIAL + 12 #:
        if (ord(c) == 59): return Font.OFFSET_SPECIAL + 13 #;
        if (ord(c) == 60): return #<
        if (ord(c) == 61): return Font.OFFSET_SPECIAL + 26 #=
        if (ord(c) == 62): return #>
        if (ord(c) == 63): return Font.OFFSET_SPECIAL + 15 #?
        if (ord(c) == 64): return #@
        if (ord(c) > 64 and ord(c) < 91): return Font.OFFSET_CAPITALS + (ord(c) - 64) #capitals
        if (ord(c) == 91): return #[
        if (ord(c) == 92): return #\
        if (ord(c) == 93): return #]
        if (ord(c) == 94): return #^
        if (ord(c) == 95): return #_
        if (ord(c) == 96): return #`
        if (ord(c) > 96 and ord(c) < 123): return Font.OFFSET_SMALL + (ord(c) - 96) #small letters
        if (ord(c) == 123): return #{
        if (ord(c) == 124): return Font.OFFSET_SPECIAL + 223 #|
        if (ord(c) == 125): return #}
        if (ord(c) == 126): return #~
        return

class Processor(object):

    def __init__(self):
        self.bbox = []
        self.lower_tresh = 255
        self.upper_tresh = 255

    def display(self, screen, image):
        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow(screen, image)
            key = cv2.waitKey(1) & 0xFF
            # escape or space
            if key == 27 or key == 32:
                break

    def update(self, screen, image, points, scale = 1):
        # draw a rectangle around the region of interest
        for pt in points:
            cv2.line(image, (int(pt[0]*scale), 0), (int(pt[0]*scale), image.shape[0]), (0, 0, 255))
            cv2.line(image, (0, int(pt[1]*scale)), (image.shape[1], int(pt[1]*scale)), (0, 0, 255))
            cv2.imshow(screen, image)

    """ Initialize the processor and show a screen to select the page boundaries """
    def init(self, page):
        image = page.getImageOriginal()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (0,0), fx=config.GUI_SCALE, fy=config.GUI_SCALE)

        prevPt = ()
        # define callback
        def click(event, x, y, flags, param):
            global prevPt
            if(len(self.bbox) < 2):
                # save the point where the click occurs
                if event == cv2.EVENT_LBUTTONDOWN:
                    prevPt = (x, y)
                # check if it was a click, not a drag
                elif event == cv2.EVENT_LBUTTONUP:
                    if prevPt == (x, y):
                        # save the coordinate
                        self.bbox.append((int(x/config.GUI_SCALE), int(y/config.GUI_SCALE)))
            self.update("page_bounds", image, self.bbox, config.GUI_SCALE)

        # select the title region
        cv2.namedWindow("page_bounds")
        cv2.setMouseCallback("page_bounds", click)
        self.display("page_bounds", image)
        cv2.destroyWindow("page_bounds")

        # set page to title crop
        page.setImageOriginal(self.crop(page.getImageOriginal(), self.bbox))

        def tresh(value):
            page.lower_tresh = cv2.getTrackbarPos("lower_tresh", "tresh")
            page.upper_tresh = cv2.getTrackbarPos("upper_tresh", "tresh")
            page.process()

        cv2.namedWindow("tresh")
        cv2.createTrackbar("lower_tresh", "tresh", page.lower_tresh, 255, tresh)
        cv2.createTrackbar("upper_tresh", "tresh", page.upper_tresh, 255, tresh)
        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            image = np.array(page.getImageProcessed())
            cv2.imshow("tresh", image)
            key = cv2.waitKey(1) & 0xFF
            # escape or space
            if key == 27 or key == 32:
                break
        self.lower_tresh = cv2.getTrackbarPos("lower_tresh", "tresh")
        self.upper_tresh = cv2.getTrackbarPos("upper_tresh", "tresh")
        cv2.destroyWindow("tresh")

    def process(self, page):
        page.setImageOriginal(self.crop(page.getImageOriginal()))
        page.lower_tresh = self.lower_tresh
        page.upper_tresh = self.upper_tresh
        return page

    def get_properties(self):
        return {
            'bbox': self.bbox,
            'lower_tresh': self.lower_tresh,
            'upper_tresh': self.upper_tresh
        }

    def set_properties(self, properties):
        self.bbox = properties['bbox']
        self.lower_tresh = properties['lower_tresh']
        self.upper_tresh = properties['upper_tresh']

    def crop(self, im, bbox = None):
        if bbox is None:
            bbox = self.bbox
        left = min(bbox[0][0], bbox[1][0])
        right = max(bbox[0][0], bbox[1][0])
        top = min(bbox[0][1], bbox[1][1])
        bottom = max(bbox[0][1], bbox[1][1])
        # crop the original image
        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        return im.crop([left, top, right, bottom])

    def average(self, boxes):
        avg = [0,0]
        for box in boxes:
            avg[0] += Box(box).getWidth()
            avg[1] += Box(box).getHeight()
        avg[0] /= len(boxes)
        avg[1] /= len(boxes)
        return avg


class Circle(Processor):

    """Processes a page by reading the file character by character and matching the OCR text until the end of the page is finished
        Current implementations breaks (keeps searching) on special characters"""
    def process(page):
        self.height = page.getImageProcessed().size[1]

        haystack = page.getCharacters()
        needle = self.text.read(1)
        prev_match = False; # combine matches into one box
        newline = False; # to put a double line at the end of a sentence (sentences end with '. ')
        instructions = []
        matches = []

        if config.DEBUGGING:
            print("Matching text...")

        ## FOR CHARACTERS
        avg = self.average(page.getCharacters()) # get average character width to calculate spaces
        if config.DEBUGGING:
            print("Average width: %r" % avg)

        for i, character in enumerate(page.getCharacters()):
            c = Character(character) #character
            if i+1 < len(page.getCharacters()):
                next_c = Character(page.getCharacters()[i+1]) #next character
            else:
                next_c = Character('None 0 0 0 0')

            #if config.DEBUGGING:
                #print(c.get())

            if needle == '.' or needle == '\n':
                newline = True

            #match character
            if newline is False and c.match(needle) is self.mode.match:
                if prev_match:
                    prev_c = matches[-1]
                    merged_c = Character([prev_c.getText() + c.getText(), prev_c.getLeft(), max(prev_c.getTop(), self.height - c.getTop()), c.getRight(), max(prev_c.getBottom(), self.height - c.getBottom())], True) #make a new character containing the previous data
                    instructions.pop() #remove the last instruction
                    matches.pop() #remove the last match
                    matches.append(merged_c)
                    instructions.append(self.generateInstruction(merged_c)) #add the instruction to the list
                else:
                    matches.append(c)
                    instructions.append(self.generateInstruction(c)) #add the instruction to the list
                prev_match = True #set prev_match to true so the next one can connect
                needle = self.text.read(1)
            else:
                prev_match = False

            #check for spaces
            if next_c.getLeft() > c.getRight() + avg[0] or next_c.getLeft() < c.getRight():
                if needle == ' ' or needle == '.' or needle == '\n':
                    instructions.append(["line", (c.getRight() + avg[0]/2, self.height - (c.getBottom() + (2*avg[1]))), (c.getRight() + avg[0]/2, self.height - (c.getBottom() - avg[1]))])
                    needle = self.text.read(1)
                if needle == ' ' or needle == '.' or needle == '\n':
                    instructions.append(["line", (c.getRight() + avg[0], self.height - (c.getBottom() + (2*avg[1]))), (c.getRight() + avg[0], self.height - (c.getBottom() - avg[1]))])
                    needle = self.text.read(1)
                while needle == ' ' or needle == '.' or needle == '\n': #skip coming newlines, dots and spaces
                    needle = self.text.read(1)
                prev_match = False
                newline = False


        if config.DEBUGGING:
            print("Done matching!")

        helpers.print_title('instructions')
        print(instructions)
        return instructions

class Cookbook(Processor):

    def __init__(self):
        super(Cookbook, self).__init__()
        self.font = Font()
        self.title_bbox = [] # bounding box for the title OCR
        self.mode = 3
        self.empty_space = []

    def init(self, page):
        im_ = page.getImageOriginal()
        super(Cookbook, self).init(page)

        page.setImageOriginal(super(Cookbook, self).crop(page.getImageOriginal()))

        #prepare an image
        image = cv2.cvtColor(np.array(page.getImageOriginal()), cv2.COLOR_RGB2BGR)
        #image = cv2.resize(image, (0,0), fx=config.GUI_SCALE, fy=config.GUI_SCALE)

        prevPt = ()
        # define callback
        def click(event, x, y, flags, param):
            global prevPt
            if(len(self.title_bbox) < 2):
                # save the point where the click occurs
                if event == cv2.EVENT_LBUTTONDOWN:
                    prevPt = (x, y)
                # check if it was a click, not a drag
                elif event == cv2.EVENT_LBUTTONUP:
                    if prevPt == (x, y):
                        # save the coordinate
                        self.title_bbox.append((x, y))
            super(Cookbook, self).update("title_bounds", image, self.title_bbox)

        # select the title region
        cv2.namedWindow("title_bounds")
        cv2.setMouseCallback("title_bounds", click)
        super(Cookbook, self).display("title_bounds", image)
        cv2.destroyWindow("title_bounds")

        # set page to title crop
        page.setImageOriginal(super(Cookbook, self).crop(page.getImageOriginal(), self.title_bbox))

        def tresh(value):
            page.lower_tresh = cv2.getTrackbarPos("lower_tresh", "tresh")
            page.upper_tresh = cv2.getTrackbarPos("upper_tresh", "tresh")
            page.process()

        cv2.namedWindow("tresh")
        cv2.createTrackbar("lower_tresh", "tresh", super(Cookbook, self).lower_tresh, 255, tresh)
        cv2.createTrackbar("upper_tresh", "tresh", super(Cookbook, self).upper_tresh, 255, tresh)
        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            image = np.array(page.getImageProcessed())
            cv2.imshow("tresh", image)
            key = cv2.waitKey(1) & 0xFF
            # escape or space
            if key == 27 or key == 32:
                break
        super(Cookbook, self).lower_tresh = cv2.getTrackbarPos("lower_tresh", "tresh")
        super(Cookbook, self).upper_tresh = cv2.getTrackbarPos("upper_tresh", "tresh")
        cv2.destroyWindow("tresh")

        #################################
        # select points for blank areas #
        #################################
        page.setImageOriginal(im_)
        page.process()
        image = np.array(page.getImageProcessed())
        image = cv2.resize(image, (0,0), fx=config.GUI_SCALE, fy=config.GUI_SCALE)
        # define callback
        def empty_space_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONUP:
                self.empty_space.append((int(x/config.GUI_SCALE), int(y/config.GUI_SCALE)))
                cv2.circle(image, (x, y), 5, 0)
                cv2.imshow("empty_space", image)

        # select the title region
        cv2.namedWindow("empty_space")
        cv2.setMouseCallback("empty_space", empty_space_click)
        super(Cookbook, self).display("empty_space", image)
        cv2.destroyWindow("empty_space")

    def process(self, page):

        # make a copy of the current image
        im_ = page.getImageOriginal()

        # crop the image
        page = super(Cookbook, self).process(page)

        # crop to title area and recognize title
        page.setImageOriginal(super(Cookbook, self).crop(page.getImageOriginal(), self.title_bbox))

        title = " ".join(page.getText().split())
        title = re.sub('[^a-zA-Z0-9- _*.]', '', title)
        print("Searching for: {0}").format(title)

        # start driver
        #https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver
        #caps = DesiredCapabilities.FIREFOX
        #caps["marionette"] = True
        driver = webdriver.Firefox()
        #driver = webdriver.Chrome() # or add to your PATH
        driver.set_page_load_timeout(15)
        driver.implicitly_wait(3) # seconds
        comments = []
        count = 0
        blogs = cookbook.search(title, driver, 5)
        for blog in blogs:
            blog_comments = cookbook.get_comments(blog, driver)
            if blog_comments is not None:
                print("Found {0} comments.").format(len(blog_comments))
                count += len(blog_comments)
                comments += blog_comments
                if(count >= 3): break #always try to fetch 4 comments

        driver.quit()

        #comments = ['comment1asdfsadfasdfas sdfasf asdfsad asdfasdf', 'comment 2',  'comment 3 Deze is te lang om sdlfkj soijsdklfj owijskljd foiwjeklj sdoifjlkwjef osijdflk weofjlksjd foiwjefkl jsdfoijlkwje fte passen']

        # find empty space on the page
        # start from top left and bottom right
        page.setImageOriginal(im_)
        page.process()
        image = np.array(page.getImageProcessed())
        #boxes = self.find_empty_space(image, [(500,150), (page.getImageProcessed().size[0] - 200, page.getImageProcessed().size[1] - 200)])
        boxes = self.find_empty_space(image, self.empty_space)
        random.shuffle(boxes)

        # fit the comments in the boxes
        # current implementation: print, if instructions are empty: skip to next box
        instructions = []
        for box in boxes:
            #instructions.append(Rect(box[0], box[1]))
            self.font.set_start((box[0]))
            self.font.set_box((box[1][0] - box[0][0], box[1][1] - box[0][1]))
            i = 0
            for comment in comments:
                print comment
                current_instruction = self.font.phrase(comment)
                if len(current_instruction) > 0:
                    instructions = instructions + current_instruction
                    self.font.current = (box[0][0], self.font.current[1] + self.font.scale * 2 * Font.LINEHEIGHT)
                    i += 1
                else:
                    break
            comments = comments[i:]

        return instructions

    def get_properties(self):
        properties = super(Cookbook, self).get_properties()
        properties['title_bbox'] = self.title_bbox
        properties['empty_space'] = self.empty_space
        return properties

    def set_properties(self, properties):
        super(Cookbook, self).set_properties(properties)
        self.title_bbox = properties['title_bbox']
        self.empty_space = properties['empty_space']

    """ return bounding boxes of emtpy space, starting from a given array of points """
    def find_empty_space(self, image, pts):

        boxes = []
        for pt in pts:
            left = {'go': True, 'point': pt[0]}
            top = {'go': True, 'point': pt[1]}
            right = {'go': True, 'point': pt[0]}
            bottom = {'go': True, 'point': pt[1]}

            # expand to top left
            while left['go'] or top['go']:
                if left['go']:
                    left['point'] -= 1
                    hits = 0
                    y = top['point']
                    while y <= bottom['point']:
                        if image[y, left['point']][0] == 0: hits += 1
                        y += 1
                    if (hits > 5) or (left['point'] <= 0): left['go'] = False
                if top['go']:
                    top['point'] -= 1
                    hits = 0
                    x = left['point']
                    while x <= right['point']:
                        if image[top['point'], x][0] == 0: hits += 1
                        x += 1
                    if (hits > 5) or (top['point'] <= 0): top['go'] = False

            # expand to bottom right
            while right['go'] or bottom['go']:
                if right['go']:
                    right['point'] += 1
                    hits = 0
                    y = top['point']
                    while y <= bottom['point']:
                        if image[y, right['point']][0] == 0: hits += 1
                        y += 1
                    if (hits > 5) or (right['point'] >= image.shape[1] - 1): right['go'] = False
                if bottom['go']:
                    bottom['point'] += 1
                    hits = 0
                    x = left['point']
                    while x <= right['point']:
                        if image[bottom['point'], x][0] == 0: hits += 1
                        x += 1
                    if (hits > 5) or (bottom['point'] >= image.shape[0] - 1): bottom['go'] = False

            # return box, add some margin
            margin = 25
            boxes.append([(left['point'], top['point']+margin), (right['point'], bottom['point']-margin)])

        return boxes

class Instructions(Processor):
    def __init__(self):
        super(Instructions, self).__init__()
        self.mode = 4
        self.verbs = None

    def init(self, page):
        super(Instructions, self).init(page)

    def load_verbs(self):
        with open("words_verbs.txt") as word_file:
            verbs = set(word.strip().lower() for word in word_file)
        with open("words_nouns.txt") as word_file:
            nouns = set(word.strip().lower() for word in word_file)
        #improve the list
        verbs = set(verbs - nouns)
        verbs = set(verbs - set(["have", "is", "are", "busy"]))
        self.verbs = set(verbs | set(["dont", "do"]))

    def is_verb(self, word):
        return word.lower() in self.verbs

    def process(self, page):
        if self.verbs is None:
            self.load_verbs()
        # crop the image
        page = super(Instructions, self).process(page)

        # iterate word by word
        match = False
        instructions = []
        prev = None # previous box
        match_str = "" # for printing
        for word in page.getWords():
            word = Box(word)
            if not match: #look for a verb
                if config.VERBOSE:
                    if match_str is not "":
                        print(match_str)
                        match_str = ""
                if self.is_verb(re.sub('[^A-Za-z0-9]+', '', word.getText())): #match
                    match = True
                else: #cross out
                    if prev is None:
                        prev = word
                    else:
                        if(word.getLeft() < prev.getRight()): #new line
                            instructions.append(prev.strike())
                            prev = word
                        else:
                            prev.setBottom(min(prev.getBottom(), word.getBottom()))
                            prev.setTop(max(prev.getTop(), word.getTop()))
                            prev.setRight(word.getRight())
            if match: #if there is a match, continue until the end of the phrase
                # first save the instructions up to then
                if prev is not None:
                    instructions.append(prev.strike())
                    prev = None
                if re.search(r'[\.,!?:;]', word.getText()) is not None:
                    match = False
                if config.VERBOSE:
                    match_str += " " + word.getText()

        return instructions

        sys.exit()
        #cv2.namedWindow("test")
        #super(Instructions, self).display("test", np.array(page.getImageProcessed()))
        print(page.getText())

        return []
