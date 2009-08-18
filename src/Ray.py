import pylab as pl

class Ray :
    ''' Class describing a light ray from an initial point to a final point '''

    def __init__(self, point, dir) :
        '''Construct a ray from a start point and direction dir'''
        print "Ray:__init__>"
        
        # initial points of the ray
        self.p0 = pl.array(point)
        self.d  = pl.array(dir)
        self.d  = self.d/pl.norm(self.d)

        # values after the ray has been propagated (empty to start with)
        self.p1 = None
        self.pha = 0        


    def propagate(self, lam) :
        return lam*self.d + self.p0

