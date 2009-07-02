import pylab as pl

class Vector :
    def __init__(self,v) :
        self.v = pl.array(v)
        
    def __str__(self) :
        return "v : "+str(self.v)
    
    def __add__(v1,v2) :
        return Vector(v1.v+v2.v)

    def __sub__(v1,v2) :
        return Vector(v1.v-v2.v)
    
    def norm(self) :
        self.v = self.v/self.mag()
        return self

    def dot(v1,v2) :
        return(pl.sum(v1.v*v2.v))
    
    def mag(self) :
        return pl.sqrt(pl.sum(self.v*self.v))

    def cross(v1,v2) :
        v = pl.zeros(len(v1.v))
        v[0] = 0.0 
        v[1] = 0.0
        v[2] = 0.0
        return Vector(v)

class Matrix : 
    def __init__(self,m) :
        self.m = pl.array(m)

    def __str__(self) :
        return "m : "+str(self.m)
        
    def __add__(m1,m2) :
        return Matrix(m1.m+m2.m)
    
    def __sub__(m1,m2) :
        return Matrix(m1.m-m2.m)

    def det(self) :
        return pl.det(self.m)

    
