from mecode import G

#font = open('fonts/ROMANS.CHR', 'r')

#font = open('fonts/hershey', 'r')

import json
import turtle

text = "Hello world!"

with open('fonts/hershey-occidental.json') as data_file:
    data = json.load(data_file)

def find(charcode):
    for glyph in data:
        if glyph['charcode'] == charcode: return glyph

def draw(glyph):
    global x;
    global y;
    for line in glyph['lines']:
        first = 1;
        for pt in line:
            if first == 1:
                first = 0
                turtle.penup()
                turtle.goto(x + pt[0] * scale, y + pt[1] * -scale)
                turtle.pendown()
            else:
                turtle.goto(x + pt[0] * scale, y + pt[1] * -scale)
    x = x + scale * (glyph['right'] - glyph['left'])

def abc():
    global y
    global x
    #l = [1, 501, 551, 601, 651, 1001, 1051, 1101]
    glyph = 1
    while True:
        if(printLetter(glyph) != False):
            printLetter(glyph+1)
            printLetter(glyph+2)
        if(x > 300):
            y = y - scale*20
            x = -300
        glyph += 50

def printLetter(charcode):
    glyph = find(charcode)
    if glyph != None: draw(glyph)
    else: return False

def demo():
    alphabet = data[:28]
    global x
    global y
    i = 1;

    for glyph in alphabet:
        draw(glyph)
        if i%10 == 0:
            y = y - scale*15
            x = 0
        i += 1

turtle.penup()
turtle.pensize(2)
scale = 2
x = -300;
y = 300;

#demo()
#for char in text:
    #print(ord(char))
    #printLetter(ord(char)+32)

abc()

turtle.done()
