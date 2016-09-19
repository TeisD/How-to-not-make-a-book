import json
import numpy as np

class Instruction(object):

    def __init__(self, type, start):
        self.type = type
        self.start = start

class Line(Instruction):

    def __init__(self, start, end):
        self.type = "line"
        self.start = start
        self.end = end

class Circle(Instruction):

    def __init__(self, start, radius):
        self.type = "circle"
        self.start = start
        self.radius = radius

class Box:

    def __init__(self, box, is_character=False):
        if is_character:
            self.box = box
        else:
            self.box = str(box).split(' ')

    def match(self, needle):
        pass

    def get(self):
        return self.box

    def getText(self):
        return str(self.box[0])

    def getLeft(self):
        return int(self.box[1])

    def getBottom(self):
        return int(self.box[2])

    def getRight(self):
        return int(self.box[3])

    def getTop(self):
        return int(self.box[4])

    def getHeight(self):
        return self.getTop() - self.getBottom()

    def getWidth(self):
        return self.getRight() - self.getLeft()

    def stroke():
        return ["circle", (box.getLeft() + box.getWidth()/2, self.height -  (box.getBottom() + box.getHeight()/2)), max(box.getHeight(), box.getWidth())/2 + config.MARGIN] # ["circle", (center), radius]

    def strike():
        return ["line", (box.getLeft(), self.height - (box.getBottom() + box.getHeight()/2)), (box.getRight(), self.height - (box.getBottom() + box.getHeight()/2))] # ["line", (start), (end)]

class Character(Box):

    def match(self, needle):
        #todo: uitbreiden naar een functie die accentjes toevoegt op karakters
        if self.getText().lower() == needle.lower():
            return True
        else:
            return False

class Font(object):

    OFFSET_SPECIAL = 700
    OFFSET_CAPITALS = 500
    OFFSET_SMALL = 600

    def __init__(self, scale = 2):
        with open('fonts/hershey-occidental.json') as data_file:
            self.font = json.load(data_file)
        self.scale = scale
        self.start = (0, 0)
        self.current = self.start

    def set_scale(self, scale):
        self.scale = scale

    def set_start(self, start):
        self.start = start
        self.current = self.start

    def phrase(self, p):
        instructions = []
        for l in p:
            print l
            instructions += self.letter(l)
        return instructions

    def letter(self, l):
        glyph = self.glyph(self.map(l))

        if glyph is None:
            self.current = (self.current[0] + self.scale * 10, self.current[1])
            return []

        instructions = []
        self.current = (self.current[0] - self.scale * glyph['left'], self.current[1])
        for line in glyph["lines"]:
            for i in range(0, len(line)-1):
                start = tuple(np.add(self.current, tuple(self.scale*x for x in tuple(line[i]))))
                end = tuple(np.add(self.current, tuple(self.scale*x for x in tuple(line[i+1]))))
                instructions.append(Line(start, end))
        self.current = (self.current[0] + self.scale * glyph['right'], self.current[1])
        return instructions

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

    def process(page):
        return [["circle", (50,50), 10], ["circle", (100,100), 10]]

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
        self.font = Font()

    def process(self, page):
        self.font.set_start((100,100))
        return self.font.phrase("Hello world!")
