import pylab as pl

from Elements import *
from Ray import *

class Source(Volume) :
    def __init__(self,name,placement) :
        self.name = name
        self.placement = placement
        self.dimension = pl.array([0.05,0.05,0.01])
        self.material = Material(Material.refract,1.0)
        self.y = 0.01

    def __str__(self) :
        s  = 'Source                   : '+self.name+'\n'
        s += 'Source.placement         : \n'+str(self.placement)
        return s

    def nextRay(self) :        
        r = Ray(self.placement.location+pl.array([0,self.y,0]),[0,0,1])
        self.y += -0.0025
        if self.y < -0.01 :
            return None
        else :
            return r
        

