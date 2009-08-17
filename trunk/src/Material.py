import pylab as pl 

class Material :

    glass  = 1
    mirror = 2
    
    def __init__(self, materialtype) :
        pass
#        if materialtype[0] == self.glass : 
#            self.refractiveindex = 0.0 
#        else if materialtype[0] == self.mirror :
#            self.refractiveindex = materialtype[1]
    
    def __str__(self) :
        s =  'Material                 :'
        return s
