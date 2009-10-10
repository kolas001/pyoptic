# $ Id: $

import numpy as np
import pylab as pl

def confocalDistance(w0, k):
    """
    Confocal distance ZC [d] from beam waist radius W0 [d] and wave number K [1/d]
    
    See also: complexBeamParameter, beamRadius
    """
    return (0.5*k)*w0**2

def complexBeamParameter(zc, z):
    """
    Complex beam parameter Q [d] from confocal distance ZC [d] and position Z [d]
    
    See also: confocalDistance
    """
    z = np.array(z)
    tmp1 = pl.zeros(z.shape, complex)
    tmp1.real = z
    zc = np.array(zc)
    tmp2 = pl.zeros(zc.shape, complex)
    tmp2.imag = zc
    return tmp1 + tmp2
    
def radiusOfCurvature(q):
    """
    Radius of curvature R [d] from complex beam parameter Q [d]
    
    See also: complexBeamParameter
    """
    invq = 1.0/q;
    idx = invq.real==0;
    if (idx.ndim == 0):
        if (idx == True):
            R = inf
        else:
            R = 1.0/invq.real
    else:
        R = pl.zeros(q.shape, double)
        R[idx] = inf
        idx = ~idx
        R[idx] = 1.0/invq[idx].real;
    return R

def beamRadius(q, k):
    """
    Beam radius W [d] from complex beam parameter Q [d] and wave number K [1/d]
    
    See also: complexBeamParameter
    """
    lam = 2.0*pi/k;
    invq = 1.0/q;
    w = sqrt(lam/(-pi*invq.imag))
    return w

def test(dryTest=True):
    dryTest = bool(dryTest)
    print "Running scalar tests ..."
    w0 = 8.0
    lam = 3.0
    zc = confocalDistance(w0, 2*pi/lam)
    assert zc == pi*w0**2/lam
    z = 0.0;
    q = complexBeamParameter(zc, z)
    assert q.real==z
    assert q.imag==zc
    R = radiusOfCurvature(q)
    assert R == inf
    w = beamRadius(q, 2*pi/lam)
    assert abs(w-w0) < 1.0e-15
    print "Pass"
    print "Running array tests ..."
    w0 = 8.0
    lam = 3.0
    zc = confocalDistance(w0, 2*pi/lam)
    assert zc == pi*w0**2/lam
    z = arange(0, 1023, 1)
    q = complexBeamParameter(zc, z)
    assert q.real[0]==z[0]
    assert q.imag[0]==zc
    R = radiusOfCurvature(q)
    assert R[0] == inf
    w = beamRadius(q, 2*pi/lam)
    assert abs(w[0]-w0) < 1.0e-15
    if not dryTest: pl.plot(z, w)
    print "Pass"

# if __name__ == "__main__":

    
