import pylab as pl

from Placement import *

class Source :
    def __init__(self,placement) :
        self.placement = placement
        print str(self)

    def __str__(self) :
        return "Source(placement="+str(self.placement)+")"

