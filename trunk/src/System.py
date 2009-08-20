import pylab as py

from Placement import *
from Source    import *
from Material  import *
from Elements  import *
from Display3D import *

# Complete optical system
class System(list) : 

    def __init__(self) :
        print "System:__init__>"

        # maximum size as determined from the elements
        self.size = [0,0,0]

    def loadSystem(self) :
        print "System:laodSystem>"

    def checkSystem(self) :
        print "System:checkSystem>"
        
    def propagate(self) :
        print "System:rayTracing>"

        raytree = []        

        # iterate over rays from source
        i = 0 
        ri = iter(self[0])
        try :                
            while True :
                r = ri.next()       
                print 'System.proagate> ray='+str(i)
                raybranch = []
                raybranch.append(r)
                for j in range(1,len(self)) :
                    print 'System.propagate> element=',j
                    rp = self[j].propagate(self[j-1],raybranch[j-1])                    
                    raybranch.append(rp)
                    print raybranch[j-1]
                    print raybranch[j]
                raytree.append(raybranch)
                i += 1
        except StopIteration :
            pass

        return raytree

                
    def __str__(self) :
        s = ''
        for e in self :
            s +=str(e)
        return s

def SystemTest() :
    print "System:SystemTest>"

    # source 
    spos = [0,0,0]
    sdir = [0,0,1]
    s0 = Source("light source",Placement(spos,sdir))

    # curved surface 
    lpos = [0,0,0.05]
    ldir = [0,0,1]
    ldim = [0.05,0.05,0.01]
    s1 = SphericalSurface("spherical 1", Volume.circ,ldim,Placement(lpos,ldir),Material(Material.refract,1.5),0.5)
    
    # plane surface
    ppos = [0,0,0.07]
    pdir = [0,0,1]
    pdim = [0.05,0.05,0.01]
    s2 = PlaneSurface("plane 1",Volume.circ,pdim,Placement(ppos,pdir),Material(Material.refract,1.0))
    
    # plane surface
    ppos = [0,0,0.25]
    pdir = [0,0,1]
    pdim = [0.05,0.05,0.01]
    s3 = PlaneSurface("plane 2",Volume.circ,pdim,Placement(ppos,pdir),Material(Material.refract,1.0))

    # system
    s = System()
    s.append(s0)
    s.append(s1)
    s.append(s2)
    s.append(s3)

    return s

    # ray trace through system
#    rl = s.propagate()
#
#    while r != None :
#        rl.append(r)
#        r1 = s[1].propagate(s[0],r)
#        print r
#        print r1[0]
#        r = s[0].nextRay()
#
#    d = Display3D(s,rl)
#    d.Draw()

    return s
