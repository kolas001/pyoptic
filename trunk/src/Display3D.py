from Elements import *
from Source import *

from enthought.mayavi import mlab
from enthought.tvtk.tools import visual

class Display3D :
    def __init__(self,s,r) :
        self.s = s
        self.r = r
        self.f = mlab.figure(size=(500,500))
        visual.set_viewer(self.f)

    def Draw(self) :
        for e in self.s :
            c = visual.color.blue
            if type(e) == Source :
                c = visual.color.red
                
            visual.box(width =e.dimension[2], 
                       height=e.dimension[0],  
                       length=e.dimension[0],
                       x     =e.placement.location[0],
                       y     =e.placement.location[1],
                       z     =e.placement.location[2],
                       representation='w',
                       color = c)                       
        pass
    
