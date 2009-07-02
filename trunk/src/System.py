import pylab as py

from Placement import *
from Source import *
from Surfaces import *
from Material import *

# Complete optical system
class System : 

    def __init__(self) :
        print "System:__init__>"

        # empty element list
        self.elist = []
        
        # maximum size as determined from the elements
        self.size = (0,0,0)

    def loadSystem(self) :
        print "System:laodSystem>"
    
    def exampleSystem(self) :
        print "System:exampleSystem>"
        # source 
        spos = (0,0,0)
        sdir = (0,0,1)
        s = Source(Placement(spos,sdir))
        
        # curved surface 
        lpos = (0,0,20)
        ldir = (0,0,1)
        ldim = (5,5)
        ss = SphericalSurface(Element(Element.circ,ldim,Placement,Material(1.5)))

        self.elist.append(s) 
        self.elist.append(ss)
