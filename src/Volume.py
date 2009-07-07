import pylab as pl

from Base      import *
from Material  import *
from Placement import *

class Volume:
    """ Orientable volume, base class to describe extent, material and orientation of a volume containing. Volume has a shape, dimension, placement and material """ 

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
