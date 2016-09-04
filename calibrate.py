# DRAW A GRID

from printer import Printer

printer = Printer()
printer.init()
printer.setTool('PEN')

# horizontal
printer.go((50,50))
printer.line((250,50))
printer.go((50,100))
printer.line((250,100))
printer.go((50,150))
printer.line((250,150))
printer.go((50,200))
printer.line((250,200))
printer.go((50,250))
printer.line((250,250))

# vertical
printer.go((50,50))
printer.line((50,250))
printer.go((100,50))
printer.line((100,250))
printer.go((150,50))
printer.line((150,250))
printer.go((200,50))
printer.line((200,250))
printer.go((250,50))
printer.line((250,250))

printer.go((50,50))
printer.circle(5)
printer.go((100,100))
printer.circle(10)
printer.go((150,150))
printer.circle(15)
printer.go((200,200))
printer.circle(20)

printer.home()
