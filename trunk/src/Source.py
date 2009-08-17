import pylab as pl

from Elements import *

class Source(Volume) :
    def __init__(self,name,placement) :
        self.name = name
        self.placement = placement

    def __str__(self) :
        s  = 'Source                   : '+self.name+'\n'
        s += 'Source.placement         : \n'+str(self.placement)
        return s

