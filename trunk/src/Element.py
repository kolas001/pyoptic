import pylab as pl

class Element :
    
    # shape of element
    rect = 0
    circ = 1 
            
    def __init__(self,shape,dimension) :
        print "Element:__init__>"
        self.shape     = shape
        self.dimension = dimension      
        
    
