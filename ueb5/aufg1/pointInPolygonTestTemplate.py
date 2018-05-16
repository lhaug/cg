from Tkinter import *
from Canvas import *
import sys

from vektor import Vektor


WIDTH  = 700 # width of canvas
HEIGHT = 700 # height of canvas

HPSIZE = 3 # half of point size (must be integer)
CLSIZE = 4 # line size
FCOLOR = "#000000" # black (fill color)
BCOLOR = "#000000" # blue (boundary color)

testPoints = False
numPolyPoints = 0

pointList = []   # list of points
elementList = [] # list of elements (used by Canvas.delete(...))


def intersect(l1, l2):
    """ returns True if linesegments l1 and l2 intersect. False otherwise."""
    #return sedgewick(l1, l2)

    v11 = Vektor(l1[0][0], l1[0][1], 1)
    v12 = Vektor(l1[1][0], l1[1][1], 1)
    v21 = Vektor(l2[0][0], l2[0][1], 1)
    v22 = Vektor(l2[1][0], l2[1][1], 1)
    #print(v11, v12, v21, v22)

    line1 = cross(v11, v12)
    line2 = cross(v21, v22)
    cut = cross(line1, line2)
    cut = cut.point()
    #print(cut)
    betw = between(cut, v11, v12, v21, v22)
    #print(betw)
    return betw

#def sedgewick(l1, l2):


def between(cut, v1, v2, v3, v4):
    erg1 = False
    erg2 = False

    # Test fuer v1, v2
    if v1.x < v2.x:
        minx = v1.x
        maxx = v2.x
    else:
        minx = v2.x
        maxx = v1.x
    if v1.y < v2.y:
        miny = v1.y
        maxy = v2.y
    else:
        miny = v2.y
        maxy = v1.y

    min = Vektor(minx, miny, 1)
    max = Vektor(maxx, maxy, 1)

    if min <= cut and max >= cut:
        erg1 = True

    # Test fuer v3, v4
    if v3.x < v4.x:
        minx = v3.x
        maxx = v4.x
    else:
        minx = v4.x
        maxx = v3.x
    if v3.y < v4.y:
        miny = v3.y
        maxy = v4.y
    else:
        miny = v4.y
        maxy = v3.y

    min = Vektor(minx, miny, 1)
    max = Vektor(maxx, maxy, 1)

    if min > max:
        min, max = max, min

    if min <= cut and max >= cut:
        erg2 = True

    #print(erg1, erg2)
    if erg1 and erg2:
        return True
    else:
        return False

def cross(p, q):

    px = p.x
    py = p.y
    pz = p.z
    qx = q.x
    qy = q.y
    qz = q.z
    a = (py * qz) - (pz * qy)
    b = (pz * qx) - (px * qz)
    c = (px * qy) - (py * qx)

    return Vektor(a, b, c)


def pointInPolygon(p):
    #print(p)
    """ test wether point p is in polygon pointList[:numPolyPoints] or not"""
    pList =  pointList[:numPolyPoints]
    pList.append(pointList[0])
    count = 0
    testLine = [p,[WIDTH, p[1]]]
    for line in zip(pList,pList[1:]):
        if intersect(line,testLine):
           count = count +1
    #print(str(count)+" count "+str((count%2) == 1))
    return (count % 2) == 1


def drawPoints():
    """ draw points """
    for p in pointList:
        if p[2]: # flag wether point is in polygon or not
            element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                          p[0]+HPSIZE, p[1]+HPSIZE,
                          fill=FCOLOR, outline=BCOLOR)
        else:
            element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                          p[0]+HPSIZE, p[1]+HPSIZE,
                          fill='', outline=BCOLOR)
	elementList.append(element)    


def drawPolygon():
    """ use first numPolyPoints points in pointlist to draw a polygon"""
    pList = [[x,y] for [x,y,z] in pointList[:numPolyPoints]]
    element = can.create_polygon(pList, fill='#AAAAAA', outline = 'black', width=3)
    elementList.append(element)   
    

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPolygon()
    drawPoints()


def switchOnTest():
    """ switch on test mode """
    global testPoints
    testPoints = True


def clearAll():
    """ clear all (point list and canvas) """
    global testPoints
    testPoints = False
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    global numPolyPoints
    # get point coordinates (Last entry: True if p is in Polygon Flase otherwise
    p = [event.x, event.y, True] 
    pointList.append(p)
    if not testPoints: # append to polygon
	    numPolyPoints = len(pointList)
    else: # test wether point is in polygon or not
	    p[2] = pointInPolygon(p)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "Test in point is in (nonconvex) polygon"
       sys.exit(-1)

    # create main window
    mw = Tk()
    mw._root().wm_title("Point in (nonconvex) polygon test")

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
    bTest = Button(cFr, text="Test points", command=switchOnTest)
    bTest.pack(side="left") 
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # start
    mw.mainloop()
    
