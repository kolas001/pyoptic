import pylab as pl

from Material  import *
from Placement import *

class Volume:
    """ Orientable volume, base class to describe extent, material and orientation of a volume containing """ 

    # shape of element
    rect = 0
    circ = 1 
            
    def __init__(self,shape,dimension,placement,material) :
        self.shape     = shape
        self.dimension = dimension
        self.placement = placement
        self.material  = material
        print str(self)

    def  __str__(self) :
        return "Volume(shape="+str(self.shape)+",dimension="+str(self.dimension)+",placement="+str(self.placement)+",material="+str(self.material)+")"
        
class PlaneSurface(Volume) :
    def __init__(self,shape,dimension,placement,material) :
        Volume.__init__(shape,dimension,placement,material)
        print str(self)
        
    def propagate(inrays) :        
        outrays = []

        for ray in inrays :
           print "Reflect"
            
           print "Refract"

    def __str__(self) :
        return "PlaneSurface("+str(Volume)+")"
            
class SphericalSurface(Volume) :
    def __init__(self,shape,dimension,placement,material,radcurv) :
        self.shape     = shape
        self.dimension = dimension
        self.placement = placement
        self.material  = material
        self.radcurv = radcurv
        print str(self)

    def propagate(inrays) :
        outrays = []
        
        for ray in inrays :
            print "Reflect" 
            
            print "Refract" 

    def __str__(self) :
        return "SphericalSurface("+Volume.__str__(self)+",radcurv="+str(self.radcurv)+")"

class CylindricalSurface(Volume) :
    def __init__(self,volume) :
        print "CylindricalSurface:__init__>"
        self.volume = volume

class AsphericalSurface(Volume) :
    def __init__(self,volume) :
        print "AsphericalSurface:__init__>"
        self.volume = volume


