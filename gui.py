import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

class Gui:

    def __init__(self):
        plt.ion()
        self.fig = plt.figure(figsize=(20,10))
        self.original = self.fig.add_subplot(1, 2, 1)
        self.original.set_title("Original page")
        self.original_img = Image.new('RGB', (1,1))
        self.processed = self.fig.add_subplot(1, 2, 2)
        self.processed.set_title("Processed page")
        self.processed_img = Image.new('RGB', (1,1))
        plt.show()

    def plot(self, instructions):
        """Generate a preview on the image. Watch out! pyocr coordinates are left top(x,y) right bottom(x,y) in a bottom-left coordinate system, PIL uses a top-left system"""
        draw = ImageDraw.Draw(self.processed_img)
        for i in instructions:
            if i.type == "line":
                draw.line([i.start, i.end], fill="red", width=2)
            elif i.type == "circle":
                draw.ellipse([i[1][0]-i[2], i[1][1]-i[2], i[1][0]+i[2], i[1][1]+i[2]], outline="red")  # left top right bottom of enclosing rectangle
            elif i.type == "rect":
                draw.rectangle([i.start, i.end], outline="red")  # left top right bottom of enclosing rectangle
        self.update()

    def setOriginal(self, image):
        self.original_img = image
        self.update()

    def setProcessed(self, image):
        self.processed_img = image
        self.update()

    def update(self):
        self.original.imshow(self.original_img, interpolation='sinc')
        self.processed.imshow(self.processed_img, interpolation='sinc')
        plt.draw()
        plt.show()
