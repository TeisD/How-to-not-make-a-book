import processor

class Watermark(object):

    def __init__(self, font, bbox):
        self.font = font
        self.bbox = bbox
        self.instructions = []

class GettyImages(Watermark):

    def __init__(self, font, bbox, author):
        Watermark.__init__(self, font, bbox)
        self.author = author

    def get(self):
        self.font.set_scale(2)
        self.font.set_offset(2000)
        word_bbox = self.font.get_word_box("gettyximages")
        self.font.set_start((self.bbox[2]-word_bbox[0],self.bbox[3]-(self.bbox[3]-self.bbox[1])/4))
        self.instructions += self.font.phrase("getty")
        self.font.set_offset(0)
        self.font.current = (self.font.current[0] - processor.Font.SPACE*self.font.scale, self.font.current[1])
        self.instructions += self.font.phrase("images")
        self.font.newline()
        self.font.set_scale(1)
        self.instructions += self.font.phrase(self.author)

        self.instructions.append(processor.Rect(
                (self.bbox[2] - word_bbox[0] - 20, self.bbox[3]-(self.bbox[3]-self.bbox[1])/4 - 20),
                (self.bbox[2], int(self.bbox[3]-(self.bbox[3]-self.bbox[1])/4 + word_bbox[1] * 2.5))
            ))

        return self.instructions

class FotoSearch(Watermark):

    def __init__(self, font, bbox):
        Watermark.__init__(self, font, bbox)

    def get(self):

        self.instructions.append(processor.Line((self.bbox[0], self.bbox[1]), (self.bbox[2], self.bbox[3])))
        self.instructions.append(processor.Line((self.bbox[2], self.bbox[1]), (self.bbox[0], self.bbox[3])))

        self.font.set_scale(3)
        self.font.set_offset(2000)
        word_bbox = self.font.get_word_box("fotosearchr")

        self.font.set_start((int(self.bbox[0] + (self.bbox[2]-self.bbox[0])/2)  - word_bbox[0]/2, int(self.bbox[1] + (self.bbox[3] - self.bbox[1])/2 - word_bbox[1]/2)))

        self.instructions += self.font.phrase("fotosearch")
        self.font.set_scale(1)
        self.font.set_offset(0)
        self.font.current = ((self.font.current[0], self.font.current[1]-processor.Font.LINEHEIGHT))
        self.instructions.append(processor.Circle(self.font.current, processor.Font.SPACE*2))
        self.font.current = ((self.font.current[0]-processor.Font.SPACE, self.font.current[1]))
        self.instructions += self.font.phrase("R")

        return self.instructions

class IStock(Watermark):

    GAP = 25

    def __init__(self, font, bbox):
        Watermark.__init__(self, font, bbox)

    def get(self):
        word_bbox = self.font.get_word_box("iStock")
        self.font.start = (self.bbox[0] + IStock.GAP, self.bbox[1] + IStock.GAP)
        self.font.current = (self.font.start[0], self.font.start[1] + word_bbox[1])

        i = 0
        while(True):
            self.instructions += self.font.phrase("iStock")
            if(self.font.current[0] + word_bbox[0]*2 > self.bbox[2]): #newline
                i += 1
                if(i%2 == 0):
                    self.font.current = (self.font.start[0], self.font.current[1] + word_bbox[0])
                else:
                    self.font.current = (self.font.start[0] + word_bbox[0], self.font.current[1] + word_bbox[0])
            else: #gap
                    self.font.current = (self.font.current[0] + word_bbox[0], self.font.current[1])

            if (self.font.current[1] > self.bbox[3] - IStock.GAP):
                break

        return self.instructions

class RF(Watermark):

    def __init__(self, font, bbox):
        Watermark.__init__(self, font, bbox)

    def get(self):

        self.font.set_scale(3)
        self.font.set_offset(2000)
        word_bbox = self.font.get_word_box("123RFr")

        self.font.set_start((int(self.bbox[0] + (self.bbox[2]-self.bbox[0])/2)  - word_bbox[0]/2, int(self.bbox[1] + (self.bbox[3] - self.bbox[1])/2 - word_bbox[1]/2)))

        self.instructions += self.font.phrase("123RF")
        self.font.set_scale(1)
        self.font.set_offset(0)
        self.font.current = ((self.font.current[0], self.font.current[1]-processor.Font.LINEHEIGHT))
        self.instructions.append(processor.Circle(self.font.current, processor.Font.SPACE*2))
        self.font.current = ((self.font.current[0]-processor.Font.SPACE, self.font.current[1]))
        self.instructions += self.font.phrase("R")

        return self.instructions

class ShutterStock(Watermark):

    def __init__(self, font, bbox):
        Watermark.__init__(self, font, bbox)

    def get(self):

        self.instructions.append(processor.Line((self.bbox[0], self.bbox[1]), (self.bbox[2], self.bbox[3])))
        self.instructions.append(processor.Line((self.bbox[2], self.bbox[1]), (self.bbox[0], self.bbox[3])))

        self.font.set_scale(3)
        self.font.set_offset(2000)
        word_bbox = self.font.get_word_box("shutterstock")

        self.font.set_start((int(self.bbox[0] + (self.bbox[2]-self.bbox[0])/2)  - word_bbox[0]/2, int(self.bbox[1] + (self.bbox[3] - self.bbox[1])/2 - word_bbox[1]/2)))

        self.instructions += self.font.phrase("shutterstock")

        return self.instructions

class Fotolia(Watermark):
    def __init__(self, font, bbox):
        Watermark.__init__(self, font, bbox)

    def get(self):
        self.font.set_scale(3)
        self.font.set_offset(2000)
        word_bbox = self.font.get_word_box("fotolia")

        self.font.set_start((int(self.bbox[0] + (self.bbox[2]-self.bbox[0])/2)  - word_bbox[0]/2, int(self.bbox[1] + (self.bbox[3] - self.bbox[1])/2 - word_bbox[1]/2)))
        self.instructions += self.font.phrase("fotolia")

        self.font.set_scale(1)
        self.font.set_offset(0)
        word_bbox = self.font.get_word_box("byadobe")
        word_bbox = (word_bbox[0] + self.font.scale*processor.Font.SPACE, word_bbox[1])
        self.font.current = (self.font.current[0] - 3*processor.Font.SPACE - word_bbox[0], self.font.current[1]+int(self.font.scale*processor.Font.LINEHEIGHT*1.5))
        self.instructions += self.font.phrase("by adobe")

        return self.instructions

class DreamsTime(Watermark):
    def __init__(self, font, bbox):
        Watermark.__init__(self, font, bbox)

    def get(self):
        radius = 25
        center = (self.bbox[0]+(self.bbox[2]-self.bbox[0])/2-radius, self.bbox[1]+(self.bbox[3]-self.bbox[1])/2-radius)
        quadrant = 1
        while(radius <= 125):
            self.instructions.append(processor.Arc(center, radius, quadrant))
            radius += (quadrant%2)*25
            center = (center[0], center[1] + (quadrant%2)*25)
            if(quadrant == 1): center = (center[0], center[1] - 50)
            quadrant += 1
            if(quadrant > 3): quadrant = 0


        word_bbox = self.font.get_word_box("dreamstime.com.")
        self.font.current = (self.bbox[2]-word_bbox[0], self.bbox[3]-word_bbox[1])
        self.instructions += self.font.phrase("dreamstime.com")

        return self.instructions
