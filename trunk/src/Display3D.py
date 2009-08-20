from System import *
from Elements import *
from Source import *

from enthought.tvtk.tools import mlab
from enthought.tvtk.tools import visual

class Display3D :
    def __init__(self,s,r) :
        self.s = s
        self.r = r
        self.f = mlab.figure()

    def Draw(self) :        

        # loop over optical elements
        for e in self.s :
            c = visual.color.blue
            if type(e) == Source :
                c = visual.color.red
                
#            b = visual.box(width =e.dimension[2], 
#                          height=e.dimension[0],  
#                          length=e.dimension[0],
#                          x     =e.placement.location[0],
#                          y     =e.placement.location[1],
#                          z     =e.placement.location[2],
#                          representation='w',
#                          color = c)                       
#            self.f.add(b)

        # loop over rays
        for r in pl.flatten(self.r) :
            if r.p1 != None :
                l = mlab.Line3([r.p0,r.p1],radius=0.0001);
                self.f.add(l)

def Display3DTest() :
    s = SystemTest()
    r = s.propagate()
    d = Display3D(s,r)
    d.Draw()
    
