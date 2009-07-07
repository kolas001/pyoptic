import pylab as pl

class Placement :
    """ Class to describe the location and orientation of a volume """

    def __init__(self, location, orientation) :
        self.location = location
        self.orientation = orientation
        print str(self)

    def __str__(self) :
        return "Placement(location="+str(self.location)+",orientation="+str(self.orientation)+")"
