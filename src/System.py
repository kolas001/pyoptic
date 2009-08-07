import pylab as py

from Base      import *
from Placement import *
from Source    import *
from Surfaces  import *
from Material  import *


# Complete optical system
class System : 

    def __init__(self) :
        print "System:__init__>"

        # empty element list
        self.vlist = []
        
        # maximum size as determined from the elements
        self.size = [0,0,0]

    def loadSystem(self) :
        print "System:laodSystem>"


    def checkSystem(self) :
        print "System:checkSystem>"
        
    def rayTrace(self) :
        print "System:rayTracing>"

    def exampleSystem(self) :
        print "System:exampleSystem>"
        # source 
        spos = [0,0,0]
        sdir = [0,0,1]
        s0 = Source(Placement(spos,sdir))
        
        # curved surface 
        lpos = [0,0,0.20]
        ldir = [0,0,1]
        ldim = [0.05,0.05]
        s1 = SphericalSurface(Volume.circ,ldim,Placement(lpos,ldir),Material((Material.glass,1.5)),20.0)

        # plane surface
        ppos = [0,0,0.25]
        pdir = [0,0,1]
        pdim = [0.05,0.05]
        s2 = PlaneSurface(Volume.circ,pdim,Placement(ppos,pdir),Material((Material.glass,1.0)))

        self.vlist.append(s0) 
        self.vlist.append(s1)
        self.vlist.append(s2)

        self.checkSystem()
