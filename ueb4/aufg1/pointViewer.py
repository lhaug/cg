from Tkinter import *
from Canvas import *
import numpy as np
import sys
import random

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

pointList = [] # list of points (used by Canvas.delete(...))

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    """ draw points """
    #for i in range(1,NOPOINTS):
	#x, y = random.randint(1,WIDTH), random.randint(1,HEIGHT)
	#p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE,
    #                       fill=COLOR, outline=COLOR)
	#pointList.insert(0,p)

    #pointList = readPoints(open(sys.argv[1])) --es muss noch von argv eingelesen werden

    points = readPoints(open("squirrel_points.raw"))

    for i in points:
        x, y = i[0], i[1]
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE, fill=COLOR, outline=COLOR)
        pointList.insert(0,p)

def rotYp():
    """ rotate counterclockwise around y axis """
    global NOPOINTS
    NOPOINTS += 100
    print "In rotYp: ", NOPOINTS
    can.delete(*pointList)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    global NOPOINTS
    NOPOINTS -= 100
    print ("In rotYn: ", NOPOINTS)
    can.delete(*pointList)
    draw()

def readPoints(file):
    points = []
    for line in file:
        points.append(list(map(lambda x: float(x), line.split())))
    return points

def boundingbox(points):

    #bounding box
    bbx = [min(x[0] for x in points), max(x[0] for x in points)]
    bby = [min(x[1] for x in points), max(x[1] for x in points)]

    return bbx, bby

    #boudingbox
    #object_bb = [map(min, zip(*points), map(max, zip(*points)))]
    #ceter of bounding box
    bb_center = [x[0]+x[1]/2.0 for x in zip(*object_bb)]
    #scale factor
    scale_factor = 2.0/max([x[1]-x[0] for x in zip(*object_bb)])

    #transform points into canonical view volume
    A = np.array([scale_factor, 0, 0, -scale_factor*bb_center[0]],
                 [0, scale_factor, 0, -scale_factor*bb_center[1]],
                 [0, 0, scale_factor, -scale_factor*bb_center[2]],
                 [0, 0, 0, 1])

    #tp = [[(p[0]-bb_center[0])*scale_factor, (p[1]-bb_center[1])*scale_factor, (p[2]-).......]]

    return object_bb




if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print ("pointViewerTemplate.py")
       sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()