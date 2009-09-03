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

    def propagate(self, d, type = 1) :
        if type == 1 : 
            i = self.fresnelSingleTransformFW(d)
        elif type == 2 :
            i = self.fresnelSingleTransformVW(d)
        elif type == 3 :
            i = self.fresnelConvolutionTransform(d)
        
        return i

    def fresnelSingleTransformFW(self,d) :
        i2 = Intensity2D(self.nx,self.startx,self.endx,
                         self.ny,self.starty,self.endy,
                         self.wl)
        u1p = self.i*pl.exp(-1j*pl.pi/(d*self.wl)*(self.xgrid**2+self.ygrid**2))
        ftu1p = pl.fftshift(pl.fft2(u1p))
        u2    = ftu1p*pl.sqrt(1j/(d*self.wl))*pl.exp(1j*pl.pi/(d*self.wl)*(i2.xgrid**2+i2.ygrid**2))
        i2.i = u2
        return i2
    
    def fresnelSingleTransformVW(self,d) :
        # compute new window
        x2 = self.nx*d*self.wl/(self.endx-self.startx)
        y2 = self.ny*d*self.wl/(self.endy-self.starty)
        
        i2 = Intensity2D(self.nx,-x2/2,x2/2,
                         self.ny,-y2/2,y2/2,
                         self.wl)
        u1p = self.i*pl.exp(-1j*pl.pi/(d*self.wl)*(self.xgrid**2+self.ygrid**2))
        ftu1p = pl.fftshift(pl.fft2(u1p))
        u2    = ftu1p*pl.sqrt(1j/(d*i2.wl))*pl.exp(1j*pl.pi/(d*i2.wl)*(i2.xgrid**2+i2.ygrid**2))
        i2.i = u2
        return i2

        # create new intensity object

        # compute intensity

        
        pass

    def fresnelConvolutionTransform(self,d) :
        pass

    def applyPhaseMap(self,pm) :
        pass
    
    def applyIntensityMap(self,im) :
        pass
#                          128                 512
# 0.01  9.99709186538e-05 0.000101681834108    0.000100494672488
# 0.025 0.000100000005848 0.000102277437825    0.000100984770495
# 0.05  0.00010000001227  0.000104085648745    0.000102679756588
# 0.075 0.000100000011289 0.000106949258587    0.00010542359127
# 0.1   0.000100000000021 0.000110786458382    0.000109137195542
# 0.5   0.000100000000191 0.000238916716463    0.00023530284487
# 1.0   0.000100000005911 0.00044307245771     0.000437005044552
# 2.0   0.000100000002613 0.000867286403545    0.000856233931076    
# 3.0   0.000100000527084 0.00129534672633     0.0012792841386
# 4.0   0.000100019612188 0.00172416963837     0.00170331074285
# 5.0   0.000100162415431 0.00215156828542     0.00212773010505 
# 6.0   0.000100641977196 0.00257316616299     0.00255234629626

def IntensityTest(d = 0.1) : 
    x = 3e-3

    i = Intensity2D(64,-x,x,
                    64,-x,x,
                    532e-9)
    #    i.makeRectangularFlatTop(0,0,0.2e-3,0.2e-3)
    i.makeGaussian(0,0,0.2e-3,0.2e-3)
    i.plot(1)
    i.calculate()
    i2 = i.propagate(d,2)
    i2.calculate()
    i2.plot(2)
    print i.xrms,i2.xrms

#    darray = []
#    xrmsarray = []
#    darray.append(0)
#    xrmsarray.append(i.xrms)

#    drange = pl.arange(0.000000001,0.5,0.005)
#    for d in drange :
#        i2 = i.propagate(d,1)
#        i2.calculate() 
#        darray.append(d)
#        xrmsarray.append(i2.xrms)
#    pl.plot(darray,xrmsarray)

    return i
