import pylab as pl 

class Material :

    mirror  = 1
    refract = 2

    def __init__(self, type, data = None) :

        self.type = type
        if self.type == self.refract :
            self.n = data
        
        pass
    
    def __str__(self) :
        s =  'Material                 : '+str(self.type)+'\n'
        if self.type == self.refract :
            s = 'Material                 : '+str(self.n)
        
        return s
