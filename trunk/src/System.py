import pylab as py

from Placement import *
from Source    import *
from Material  import *
from Elements  import *

# Complete optical system
class System(list) : 

    def __init__(self) :
        print "System:__init__>"

        # maximum size as determined from the elements
        self.size = [0,0,0]

    def loadSystem(self) :
        print "System:laodSystem>"

    def checkSystem(self) :
        print "System:checkSystem>"
        
    def rayTrace(self) :
        print "System:rayTracing>"

    def __str__(self) :
        s = ''
        for e in self :
            s +=str(e)
        return s

def exampleSystem() :
    print "System:exampleSystem>"
    # source 
    spos = [0,0,0]
    sdir = [0,0,1]
    s0 = Source("light source",Placement(spos,sdir))

    # curved surface 
    lpos = [0,0,0.20]
    ldir = [0,0,1]
    ldim = [0.05,0.05,0.01]
    s1 = SphericalSurface("spherical 1", Volume.circ,ldim,Placement(lpos,ldir),Material(Material.refract,1.5),20.0)
    
    # plane surface
    ppos = [0,0,0.25]
    pdir = [0,0,1]
    pdim = [0.05,0.05,0.01]
    s2 = PlaneSurface("plane 1",Volume.circ,pdim,Placement(ppos,pdir),Material(Material.refract,1.0))
        
    # system
    s = System()
    s.append(s0)
    s.append(s1)
    s.append(s2)

    # ray trace through system
    

    return s
