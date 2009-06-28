import pylab as pl

class Vector :
    def __init__(self,v) :
        self.v = pl.array(v)
        
    def __str__(self) :
        return "v : "+str(self.v)
    
    def __add__(v1,v2) :
        return Vector(v1.v+v2.v)
    
    def norm(self) :
        self.v = self.v/pl.float64(pl.sum(self.v))
        return self

    def dot(v1,v2) :
        return(pl.sum(v1.v*v2.v))
    
    def cross(v1,v2) :
        v = pl.zeros(len(v1.v))
        v[0] = 0.0 
        v[1] = 0.0
        v[2] = 0.0
        return Vector(v)

class Matrix : 
    def __init__(self,m) :
        self.m = m
