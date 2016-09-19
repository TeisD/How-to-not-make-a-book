from mecode import G
import json
import turtle

text = "Hello world! 123 ABC"

with open('fonts/hershey-occidental.json') as data_file:
    data = json.load(data_file)

def find(charcode):
    for glyph in data:
        if glyph['charcode'] == charcode: return glyph

def draw(glyph):
    global x;
    global y;
    if glyph is None:
        x += 20
        return

    x -= scale * glyph['left']
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

    x += scale * glyph['right']

def abc():
    global y
    global x
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

def map(c):
    OFFSET_SPECIAL = 700
    OFFSET_CAPITALS = 500
    OFFSET_SMALL = 600
    if (ord(c) < 33): return #unused
    if (ord(c) == 33): return OFFSET_SPECIAL + 14 #!
    if (ord(c) == 34): return OFFSET_SPECIAL + 17 #"
    if (ord(c) == 35): return OFFSET_SPECIAL + 33 ##
    if (ord(c) == 36): return OFFSET_SPECIAL + 19 #$
    if (ord(c) == 37): return #%
    if (ord(c) == 38): return OFFSET_SPECIAL + 34 #&
    if (ord(c) == 39): return OFFSET_SPECIAL + 16 #'
    if (ord(c) == 40): return OFFSET_SPECIAL + 21 #(
    if (ord(c) == 41): return OFFSET_SPECIAL + 22 #)
    if (ord(c) == 42): return OFFSET_SPECIAL + 28 #*
    if (ord(c) == 43): return OFFSET_SPECIAL + 25 #+
    if (ord(c) == 44): return OFFSET_SPECIAL + 11 #,
    if (ord(c) == 45): return OFFSET_SPECIAL + 24 #-
    if (ord(c) == 46): return OFFSET_SPECIAL + 10 #.
    if (ord(c) == 47): return OFFSET_SPECIAL + 20 #/
    if (ord(c) > 47 and ord(c) < 58): return OFFSET_SPECIAL + (ord(c) - 48) #numbers
    if (ord(c) == 58): return OFFSET_SPECIAL + 12 #:
    if (ord(c) == 59): return OFFSET_SPECIAL + 13 #;
    if (ord(c) == 60): return #<
    if (ord(c) == 61): return OFFSET_SPECIAL + 26 #=
    if (ord(c) == 62): return #>
    if (ord(c) == 63): return OFFSET_SPECIAL + 15 #?
    if (ord(c) == 64): return #@
    if (ord(c) > 64 and ord(c) < 91): return OFFSET_CAPITALS + (ord(c) - 64) #capitals
    if (ord(c) == 91): return #[
    if (ord(c) == 92): return #\
    if (ord(c) == 93): return #]
    if (ord(c) == 94): return #^
    if (ord(c) == 95): return #_
    if (ord(c) == 96): return #`
    if (ord(c) > 96 and ord(c) < 123): return OFFSET_SMALL + (ord(c) - 96) #small letters
    if (ord(c) == 123): return #{
    if (ord(c) == 124): return OFFSET_SPECIAL + 223 #|
    if (ord(c) == 125): return #}
    if (ord(c) == 126): return #~
    return

def string(s):
    for c in s:
        draw(find(map(c)))

turtle.penup()
turtle.pensize(2)
scale = 2
x = -300;
y = 300;

#demo()
#for char in text:
    #print(ord(char))
    #printLetter(ord(char)+32)

#abc()

string(text)

turtle.done()
