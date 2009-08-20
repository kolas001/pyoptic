import pylab as pl

from Material  import *
from Placement import *
from Ray       import *

class Volume() :
    ''' Orientable volume, base class to describe extent, material and orientation of a volume containing ''' 

    # shape of element
    rect = 0
    circ = 1 
            
    def __init__(self,name, shape,dimension,placement,material) :
        self.name      = name
        self.shape     = shape
        self.dimension = pl.array(dimension)
        self.placement = placement
        self.material  = material

    def  __str__(self) :
        s  = 'Volume\n'
        s += 'Volume.shape             : '+str(self.shape)+'\n'
        s += 'Volume.dimension         : '+str(self.dimension)+'\n'
        s += 'Volume.placement         : \n'+str(self.placement)
        s += 'Volume.material          : \n'+str(self.material)
        return s

class OpticalSurface(Volume) :
    def __init__(self) :
        pass

    def proagate(self,previous,inray) :
        # compute intersection
        self.intersection(inray)                    
        # compute normal
        sn = self.surfaceNormal(inray.p1)            
        # compute out going ray
        outray = snell(inray,sn,previous.material,self.material)
        
    def intersection(self,inray) :
        pass
    def surfaceNormal(self,inray) :
        pass

class PlaneSurface(Volume) :
    def __init__(self,name,shape,dimension,placement,material) :
        Volume.__init__(self,name,shape,dimension,placement,material)
        
    def propagate(self,previous,inray) :        
            
        outray = inray

        # compute intersection
        self.intersection(inray)                    
        # compute normal
        sn = self.surfaceNormal(inray.p1)            
        # compute out going ray
        outray = snell(inray,sn,previous.material,self.material)

        return outray

    def intersection(self,inray) :
        lam = pl.linalg.dot(self.placement.location,inray.p0)/pl.linalg.dot(self.placement.orientation,self.placement.location)
        inray.p1 = inray.propagate(lam)
        
    
    def surfaceNormal(self,inray) :
        return self.placement.orientation
    
    
    def __str__(self) :
        s  = 'PlaneSurface             : '+self.name+'\n'
        s += 'PlaneSurface.Volume      :\n'+Volume.__str__(self)
        return s
            
class SphericalSurface(Volume) :
    def __init__(self,name,shape,dimension,placement,material,radcurv) :
        Volume.__init__(self,name,shape,dimension,placement,material)
        self.radcurv   = radcurv


    def propagate(self,previous,inray) :
#        if type(inrays) != list :
#            inrays = [inrays]
            
        outrays = []
        
        # compute intersection
        self.intersection(inray)                    
        # compute normal
        sn = self.surfaceNormal(inray.p1)            
        # compute out going ray
        outray = snell(inray,sn,previous.material,self.material)

        # append rays
        outrays.append(outray)
            
        return outray

    def intersection(self,ray) :
#        c   = pl.dot(ray.p0,ray.p0)-self.radcurv**2-pl.dot(self.placement.location,self.placement.location)
#        b   = 2*pl.dot(ray.p0,ray.d)
#        a   = 1 
        # centre vector
        cv = self.placement.location+self.placement.orientation*self.radcurv
        # coefficients of quadratic equation
        a = 1 
        b = 2*pl.dot(ray.d,ray.p0-cv)
        c = -2*pl.dot(ray.p0,cv)+pl.dot(cv,cv)-self.radcurv**2
        print cv
        qs  = b**2-4*a*c
        if qs == 0 :
            lam = -b/(2*a)
        elif qs < 0 :
            lam = None
        else :
            lamp = (-b+pl.sqrt(b**2-4*a*c))/(2*a)
            lamn = (-b-pl.sqrt(b**2-4*a*c))/(2*a)
            pd   = pl.linalg.norm(ray.propagate(lamp)-ray.p0)
            nd   = pl.linalg.norm(ray.propagate(lamn)-ray.p0)
            lam = min(lamp,lamn)

            # assign intersection
        ray.p1 = ray.propagate(lam)
    
    def surfaceNormal(self, p1) :
        cv = self.placement.location+self.placement.orientation*self.radcurv
        sn = p1-cv
        sn = -sn/pl.linalg.norm(sn)
        return sn

    def reflection(self,ray) :
        pass 

    def refraction(self,previous, ray) :
        pass
    
    def __str__(self) :
        s  = 'SphericalSurface         : '+self.name+'\n'
        s += 'SphericalSurface.volume  : \n'+Volume.__str__(self)+'\n'
        s += 'SphericalSurface.radcurv : '+str(self.radcurv)+'\n'
        return s

class CylindricalSurface(Volume) :
    def __init__(self,volume) :
        print 'CylindricalSurface.__init__>'
        self.volume = volume

class EvenAsphericalSurface(Volume) :
    def __init__(self,volume) :
        print 'AsphericalSurface.__init__>'
        self.volume = volume

class OddAsphericalSurface(Volume) :
    def __init__(self,volume) :
        print 'AsphericalSurface.__init__>'
        self.volume = volume

class ThinLens(Volume) :
    def __init__(self,volume) :
        print 'ThisLens.__init__>'

def snell(ray,sn,material1,material2) :
    n1 = material1.n
    n2 = material2.n

    nr = n1/n2
    dp  = pl.dot(ray.d,sn)
    gam = ((nr*dp)**2-(n1/n2)+1)**0.5 - nr*dp
    # new direction
    d2  = ray.d*n1/n2+gam*sn
    d2 = d2/pl.linalg.norm(d2)
    r = Ray(ray.p1,d2)

    print 'snell> in\n',ray
    print 'snell> normal ',sn
    print 'snell> material 1',material1
    print 'snell> material 2', material2
    print 'snell> out',r
    return r
    
def reflect(ray,sn) :
    d2 = ray.d-2*pl.dot(ray.d,sn)*sn
    r = Ray(ray.p1,d2)
    return r

