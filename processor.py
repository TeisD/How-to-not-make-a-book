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

    def process(self, page):
        return super(Cookbook, self).process()

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

