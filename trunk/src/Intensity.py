import pylab as pl

############################################################################
# Two dimensional Intensity distribution (plane uniform grid)
############################################################################            
class Intensity2D :
    def __init__(self, 
                 nx = 5012, startx = -1e-3, endx = 1e-3, 
                 ny = 5012, starty = -1e-3, endy = 1e-3, 
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
        self.i = pl.zeros((self.nx,self.ny))

    def makeGaussian(self,mx,my,sx,sy) :
        print "Intensity:Intensity2D:makeGaussian",mx,my,sx,sy
        self.i = 1/(sx*sy*2*pl.pi)*pl.complex64(pl.exp(-((self.xgrid-mx)**2/(2*sx**2))-((self.ygrid-my)**2/(2*sy**2))))

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
        a = rx*ry
        self.i = pl.complex64( (self.xgrid>=-rx/2+mx) & 
                               (self.xgrid<=rx/2+mx)  & 
                               (self.ygrid>=-ry/2+my) &
                               (self.ygrid<=ry/2+my) )/a

    def makeHermiteGaussian(self) :
        pass
    
    def makeLagurreGaussian(self) :
        pass
    
    def plot(self,f) :
        print "Intensity:Intensity2D:plot"
        self.project()

        pl.figure(f)
        pl.clf()

        pl.subplot(2,2,1) 
        pl.contourf(self.xgrid,self.ygrid,self.i*self.i.conj())
        pl.xlim(self.startx,self.endx)
        pl.ylim(self.starty,self.endy)
        pl.colorbar()
        pl.subplot(2,2,2)
        pl.plot(self.yproj,self.y)
        pl.ylim(self.starty,self.endy)
        pl.subplot(2,2,3)
        pl.plot(self.x,self.xproj)
        pl.xlim(self.startx,self.endx)
        pl.subplot(2,2,4)
#        pl.contourf(self.xgrid,self.ygrid,pl.arctan2(self.i.imag,self.i.real))
#        pl.xlim(self.startx,self.endx)
#        pl.ylim(self.starty,self.endy)
#        pl.colorbar()
    
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

    def propagate(self, d, type = 1) :
        if type == 1 : 
            i2 = self.fresnelSingleTransformFW(d)
        elif type == 2 :
            i2 = self.fresnelSingleTransformVW(d)
        elif type == 3 :
            i2 = self.fresnelConvolutionTransform(d)
        
        return i2

    def fresnelSingleTransformFW(self,d) :
        i2 = Intensity2D(self.nx,self.startx,self.endx,
                         self.ny,self.starty,self.endy,
                         self.wl)
        u1p = self.i*pl.exp(-1j*pl.pi/(d*self.wl)*(self.xgrid**2+self.ygrid**2))
        ftu1p = pl.fftshift(pl.fft2(u1p))
        u2    = ftu1p*1j/(d*self.wl)*pl.exp(1j*pl.pi/(d*self.wl)*(self.xgrid**2+self.ygrid**2))
        i2.i = u2
        return i2
    
    def fresnelSingleTransformVW(self,d) :
        # compute new window
        x2 = self.nx*d*self.wl/(self.endx-self.startx)
        y2 = self.ny*d*self.wl/(self.endy-self.starty)

        # create new intensity object
        i2 = Intensity2D(self.nx,-x2/2,x2/2,
                         self.ny,-y2/2,y2/2,
                         self.wl)

        # compute intensity
        u1p = self.i*pl.exp(-1j*pl.pi/(d*self.wl)*(self.xgrid**2+self.ygrid**2))
        ftu1p = pl.fftshift(pl.fft2(u1p))
        u2    = ftu1p*1j/(d*i2.wl)*pl.exp(1j*pl.pi/(d*i2.wl)*(i2.xgrid**2+i2.ygrid**2))
        i2.i = u2

        return i2

    def fresnelConvolutionTransform(self,d) :
        # make intensity distribution
        i2 = Intensity2D(self.nx,self.startx,self.endx,
                         self.ny,self.starty,self.endy,
                         self.wl)       

        # FT on inital distribution 
        u1ft = pl.fftshift(pl.fft2(self.i))

        # 2d convolution kernel
        k = 2*pl.pi/self.wl
        
        # make spatial frequency matrix
        maxsfx = 2*pl.pi/self.dx
        maxsfy = 2*pl.pi/self.dy
        
        dsfx = 2*maxsfx/(self.nx)
        dsfy = 2*maxsfy/(self.ny)
        
        self.sfx = pl.arange(-maxsfx,maxsfx+1e-15,dsfx)
        self.sfy = pl.arange(-maxsfy,maxsfy+1e-15,dsfy)
        
        print len(self.sfx),len(self.sfy)

        [self.sfxgrid, self.sfygrid] = pl.meshgrid(self.sfx,self.sfy)
                
        # make convolution kernel 
        kern = pl.exp(1j*d*(self.sfxgrid**2+self.sfygrid**2)/(2*k))
        
        # apply convolution kernel and invert
        i2.i = pl.ifft2(kern*u1ft) 

        return i2

    def applyPhaseMap(self,pm) :
        pass
    
    def applyIntensityMap(self,im) :
        pass

############################################################################
# Unit test algorithms.
############################################################################

def fresnelSingleTransformVWTest(d) :
    x = 1.5e-3
    i = Intensity2D(1024,-x/2,x/2,
                    1024,-x/2,x/2,
                    532e-9)
    #    i.makeGaussian(0,0,0.2e-3,0.2e-3)
    i.makeRectangularFlatTop(0,0,0.2e-3,0.2e-3)
    i.plot(1)
    i.calculate()
    
    i2 = i.propagate(d,2)
    i2.calculate()
    i2.plot(2)

def fresnelConvolutionTransformTest(d) :
    x = 1.5e-3
    i = Intensity2D(1024,-x/2,x/2,
                    1024,-x/2,x/2,
                    532e-9)
    #    i.makeGaussian(0,0,0.1e-3,0.1e-3)
    i.makeRectangularFlatTop(0,0,0.2e-3,0.2e-3)
    i.plot(1)
    i.calculate()
    
    i2 = i.propagate(d/2.0,3)
    i2.plot(2)
    i3 = i2.propagate(d/2.0,3)
    
    i3.calculate()
    i3.plot(3)

    i4 = i.propagate(d,3)
    i4.calculate()
    i4.plot(4)

def methodCompare() :
    x = 2e-3
    d = 0.0078125
    i = Intensity2D(1024,-x/2,x/2,
                    1024,-x/2,x/2,
                    500e-9)
    i.makeRectangularFlatTop(0,0,0.2e-3,0.2e-3)
    i.calculate()

    i2 = i.propagate(d,1)
    i2.calculate()
#    i2.plot(1)


    i3 = i.propagate(d,2)
    i3.calculate()
#    i3.plot(2)

    i4 = i.propagate(d/4,3)
    i4.calculate()

    pl.figure(3)
    
    pl.subplot(2,2,1)
    pl.plot(i.x,i.xproj/max(i.xproj))
    pl.subplot(2,2,2)
    pl.plot(i2.x,i2.xproj/max(i2.xproj))
    pl.subplot(2,2,3)
    pl.plot(i3.x,i3.xproj/max(i3.xproj))
    pl.subplot(2,2,4)
    pl.plot(i2.x,i2.xproj/max(i2.xproj))
    pl.plot(i4.x,i4.xproj/max(i4.xproj))

    
