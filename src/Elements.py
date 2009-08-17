import pylab as pl

from Material  import *
from Placement import *

class Volume:
    """ Orientable volume, base class to describe extent, material and orientation of a volume containing """ 

    # shape of element
    rect = 0
    circ = 1 
            
    def __init__(self,name, shape,dimension,placement,material) :
        self.name      = name
        self.shape     = shape
        self.dimension = pl.array(dimension)
        self.placement = placement
        self.material  = material

    def  __str__(self) :
        s  = 'Volume\n'
        s += 'Volume.shape             : '+str(self.shape)+'\n'
        s += 'Volume.dimension         : '+str(self.dimension)+'\n'
        s += 'Volume.placement         : \n'+str(self.placement)
        s += 'Volume.material          : \n'+str(self.material)


        return s 
        
class PlaneSurface(Volume) :
    def __init__(self,name,shape,dimension,placement,material) :
        Volume.__init__(self,name,shape,dimension,placement,material)
        
    def propagate(inrays) :        
        outrays = []

        for ray in inrays :
           print "Reflect"
            
           print "Refract"

    def __str__(self) :
        s  = 'PlaneSurface             : '+self.name+'\n'
        s += 'PlaneSurface.Volume      :\n'+Volume.__str__(self)
        return s
            
class SphericalSurface(Volume) :
    def __init__(self,name,shape,dimension,placement,material,radcurv) :
        self.name      = name
        self.shape     = shape
        self.dimension = dimension
        self.placement = placement
        self.material  = material
        self.radcurv   = radcurv

    def propagate(inrays) :
        outrays = []
        
        for ray in inrays :
            print "Reflect" 
            
            print "Refract" 

    def __str__(self) :
        s  = 'SphericalSurface         : '+self.name+'\n'
        s += 'SphericalSurface.volume  : \n'+Volume.__str__(self)+'\n'
        s += 'SphericalSurface.radcurv : '+str(self.radcurv)+'\n'
        return s

class CylindricalSurface(Volume) :
    def __init__(self,volume) :
        print "CylindricalSurface:__init__>"
        self.volume = volume

class AsphericalSurface(Volume) :
    def __init__(self,volume) :
        print "AsphericalSurface:__init__>"
        self.volume = volume


