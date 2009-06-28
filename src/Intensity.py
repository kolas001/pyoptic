import pylab as pl

class Intensity2D :
    def __init__(self, 
                 nx = 64, startx = -1e-3, endx = 1e-3, 
                 ny = 64, starty = -1e-3, endy = 1e-3, 
                 wl=532e-9) :
        self.nx     = nx
        self.startx = pl.double(startx)
        self.endx   = pl.double(endx)
        self.ny     = ny
        self.starty = pl.double(starty)
        self.endy   = pl.double(endy)
        self.wl     = wl 

        print "Intensity:Intensity2D:__init__",self.nx,self.startx,self.endx,self.ny,self.starty,self.endy,self.wl

        # make grid
        self.grid()
        
    def grid(self) :
        print "Intensity:Intensity2D:grid"
        self.x  = pl.arange(self.startx,self.endx+1e-15,(self.endx-self.startx)/(self.nx-1))
        self.y  = pl.arange(self.starty,self.endy+1e-15,(self.endy-self.starty)/(self.ny-1))
        self.dx = self.x[1]-self.x[0]
        self.dy = self.y[1]-self.y[0]
        self.nx = len(self.x)
        self.ny = len(self.y)
        [self.xgrid, self.ygrid] = pl.meshgrid(self.x,self.y)
        print "Intensity:Intensity2D:grid>",self.nx,self.ny,self.dx,self.dy
        

    def makeGaussian(self,mx,my,sx,sy) :
        print "Intensity:Intensity2D:makeGaussian",mx,my,sx,sy
        self.i = pl.complex64(pl.exp(-((self.xgrid-mx)/sx)**2-((self.ygrid-my)/sy)**2))

    def makeEllipticalFlatTop(self,mx,my,rx,ry) :
        print "Intensity:Intensity2D:makeEllipticalFlatTop",mx,my,rx,ry
        mx = pl.double(mx)
        my = pl.double(my)
        rx = pl.double(rx)
        ry = pl.double(ry)

        self.i = pl.complex64( ((self.xgrid-mx)/rx)**2 + ((self.ygrid-my)/ry)**2 <= 1.0) 

    def makeRectangularFlatTop(self,mx,my,rx,ry) :
        print "Intensity:Intensity2D:makeRectangularFlatTop",mx,my,rx,ry
        
        rx = pl.double(rx)
        ry = pl.double(ry)
        self.i = pl.complex64( (self.xgrid>=-rx/2+mx) & 
                               (self.xgrid<=rx/2+mx)  & 
                               (self.ygrid>=-ry/2+my) &
                               (self.ygrid<=ry/2+my) )
        
    def plot(self,f) :
        print "Intensity:Intensity2D:plot"
        self.project()

        pl.figure(f)
        pl.clf()

        pl.subplot(2,2,1) 
        pl.contourf(self.xgrid,self.ygrid,self.i*self.i.conj())
        pl.xlim(self.startx,self.endx)
        pl.ylim(self.starty,self.endy)
#        pl.colorbar()
        pl.subplot(2,2,2)
        pl.plot(self.yproj,self.y)
        pl.ylim(self.starty,self.endy)
        pl.subplot(2,2,3)
        pl.plot(self.x,self.xproj)
        pl.xlim(self.startx,self.endx)
        pl.subplot(2,2,4)
        pl.contourf(self.xgrid,self.ygrid,pl.arctan2(self.i.imag,self.i.real))
        pl.xlim(self.startx,self.endx)
        pl.ylim(self.starty,self.endy)
        pl.colorbar()
    
    def project(self) :
        print "Intensity:Intensity2D:project"
        self.xproj = pl.sum(abs(self.i)**2,0)
        self.yproj = pl.sum(abs(self.i)**2,1)
        
    def calculate(self) :
        print "Intensity:Intensity2D:calcaulate"
        self.project()
        self.sum   = pl.sum(self.xproj)
        self.xmean = pl.sum(self.xproj*self.x)/pl.sum(self.xproj)
        self.ymean = pl.sum(self.yproj*self.y)/pl.sum(self.yproj)
        self.xrms  = pl.sqrt(pl.sum(self.xproj*self.x**2)/self.sum)
        self.yrms  = pl.sqrt(pl.sum(self.yproj*self.y**2)/self.sum)

        print "Intensity:Intensity2D:calculate ",self.xmean,self.ymean,self.xrms,self.yrms
        
