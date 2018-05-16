from Tkinter import *
from Canvas import *
import sys
from copy import deepcopy


WIDTH  = 700 # width of canvas
HEIGHT = 700 # height of canvas

HPSIZE = 3 # half of point size (must be integer)
CLSIZE = 4 # clip line size
FCOLOR = "#000000" # black (fill color)
BCOLOR = "#000000" # blue (boundary color)

clipRegion = [] # clipping rectangle

pointList = []   # list of points
elementList = [] # list of elements (used by Canvas.delete(...))


class Point:
    """ Point consists of coordinates and region code """
    def __init__(self, co, cr):
	self.coords = co
	# region code 
	self.reCode = 8*(co[1]<cr[1][1])+4*(co[1]>cr[0][1])+2*(co[0]>cr[1][0])+(co[0]<cr[0][0])


def normalizeClipRegion(clipRegion):
    """ normalize clip region to point list [lower left, upper right] """
    ll = map(min,apply(zip,clipRegion)) # lower left corner
    ur = map(max,apply(zip,clipRegion)) # upper right corner
    return [[ll[0],ur[1]], [ur[0],ll[1]]]


def drawPoints():
    """ draw points """
    for p in pointList:
        element = can.create_oval(p.coords[0]-HPSIZE, p.coords[1]-HPSIZE,
                                      p.coords[0]+HPSIZE, p.coords[1]+HPSIZE,
                                      fill=FCOLOR, outline=BCOLOR)
        elementList.append(element)


def drawBox():
    """ use first and second point in pointlist to draw a box"""
    if len(pointList) >1:
        element = can.create_rectangle(pointList[0].coords,pointList[1].coords, width=3)
        elementList.append(element)   

    
def drawLines():
    """ use third and next points in pointlist to draw lines"""
    for line in zip(pointList[2::2],pointList[3::2]):
        lc = lineCase(line)
        if lc == 0:
            print "line complete inside rectangle!"
            element = can.create_line(line[0].coords, line[1].coords, width=CLSIZE)
            elementList.append(element)
        elif lc == -1:
            print "line not visible!"
            element = can.create_line(line[0].coords, line[1].coords, width=1)
            elementList.append(element)
        else:
            print "need further tests... linecode: ", lc
            element = can.create_line(line[0].coords, line[1].coords, width=1)
            elementList.append(element)
            newLine = calcNewLine(line, lc, clipRegion)
            if newLine:
                print("geklappt")
                element = can.create_line(newLine, width=CLSIZE)
                elementList.append(element)


def lineCase(line):
    """ Cohen-Sutherland Algorithm. Use region codes of line points to determine wether
        1. both points -> line lies completly inside the clipping region
	    2. both points -> line lies complety on one side of the clipping region
	    3. Otherwise """
    union = line[0].reCode | line[1].reCode
    sect  = line[0].reCode & line[1].reCode
    # 2. case
    if sect != 0:
        # line is completly unvisible
        return -1
    # 1. and 3. case
    else:
        # if union == 0 line is completly visible
        # othervise furhter tests are nessecary
        print(int2bin4(union))
        return union
	
    
def calcNewLine(Line, lineC, clipRegion):
    """ Calculate clipped line """
    # TODO: calculate new line (clipped at clipRegion)
    if lineC == -1:
        return[]
    if lineC == 0:
        return Line
    else:
        if (lineC & 0x8):   #SP mit ymax
            new = sp_y(Line, clipRegion[1][1])
            print(1)
            return calcNewLine(new, lineC-8, clipRegion)
        elif (lineC & 0x4):   #SP mit ymin
            new = sp_y(Line, clipRegion[0][1])
            print(2)
            return calcNewLine(new, lineC-4, clipRegion)
        elif (lineC & 0x2):   #SP mit xmax
            print(3)
            new = sp_x(Line, clipRegion[1][0])
            return calcNewLine(new, lineC-2, clipRegion)
        elif (lineC & 0x1):   #SP mit xmin
            print(4)
            new = sp_x(Line, clipRegion[0][0])
            return calcNewLine(new, lineC-1, clipRegion)
        return []

def sp_x(line, x):
    x1 = line[0].coords[0]
    x2 = line[1].coords[0]
    y1 = line[0].coords[1]
    y2 = line[1].coords[1]
    y_new = ((y2-y1)/(x2-x1))*(x-x2)+y2
    line[0].coords = [x, y_new]
    return line

def sp_y(line, y):
    x1 = line[0].coords[0]
    x2 = line[1].coords[0]
    y1 = line[0].coords[1]
    y2 = line[1].coords[1]
    x_new = ((x2-x1)/(y2-y1))*(y-y2)*x2
    line[1].coords = [x_new, y]
    return line


def int2bin4(i):
    s = [0,0,0,0]
    for x in range(0,4):
        if i == 0:
            s[x] = 0
        s[x] = i%2
        i = int(i)/int(2)
    return s
    

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints()
    drawBox()
    drawLines()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    #print "left mouse button clicked at ", event.x, event.y
    global clipRegion
    p = [event.x, event.y]
    if len(pointList) < 2: 
	    point = Point(p, [[0,0],[WIDTH,HEIGHT]])
    elif len(pointList) == 2:
	    clipRegion = normalizeClipRegion([pointList[0].coords, pointList[1].coords])
 	    point = Point(p, clipRegion)
    else:
	    point = Point(p, clipRegion)
    pointList.append(point)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "LineClipping"
       sys.exit(-1)

    # create main window
    mw = Tk()
    mw._root().wm_title("Line clipping (Cohen-Sutherland Algorithm)")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>",mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left") 
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # start
    mw.mainloop()
    
