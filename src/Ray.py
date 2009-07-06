import pylab as pl

class Ray :
    """ Class describing a light ray from an initial point to a final point """

    def __init__(self, point, dir) :
        print "Ray:__init__>"
        
        # initial points of the ray
        self.p0 = point 
        self.d  = dir

        # values after the ray has been propagated
        self.p1 = pl.array([])
        self.pha = 0 
