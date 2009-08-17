import pylab as pl

from Volume import *

class Source(Volume) :
    def __init__(self,placement) :
        self.placement = placement
        print str(self)

    def __str__(self) :
        return "Source(placement="+str(self.placement)+")"

