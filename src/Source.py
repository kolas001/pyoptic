import pylab as pl

from Elements import *
from Ray import *
from Placement import *

class Source(Volume,list) :
    def __init__(self,name,placement) :
        print 'Source.__init__'
        self.name = name
        self.placement = placement
        self.dimension = pl.array([0.05,0.05,0.01])
        self.material = Material(Material.refract,1.0)
        self.exampleRays()

    def __str__(self) :
        s  = 'Source                   : '+self.name+'\n'
        s += 'Source.placement         : \n'+str(self.placement)
        return s
    
    def exampleRays(self,d=0.01) :
        r0  = Ray(self.placement.location,[0,0,1])
        ryp = Ray(self.placement.location+pl.array([0,d,0]),[0,0,1])
        ryn = Ray(self.placement.location+pl.array([0,-d,0]),[0,0,1])
        rxp = Ray(self.placement.location+pl.array([d,0,0]),[0,0,1])
        rxn = Ray(self.placement.location+pl.array([-d,0,0]),[0,0,1])
        self.append(r0)
        self.append(ryp)
        self.append(ryn)
        self.append(rxp)
        self.append(rxn)
        

def SourceTest() :
    s = Source("test",Placement([0,0,0],[0,0,1]))
    s.exampleRays()
    return s
