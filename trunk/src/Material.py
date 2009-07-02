import pylab as pl 

class Material :
    def __init__(self, refindex) :
        print "Material:__init__>"
        if type(refindex) == float :
            self.refindex = refindex
