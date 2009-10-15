# $ Id: $

import numpy as np
import pylab as pl

class GaussianBeam:
    def __init__(self, w0z0, k):
        """
        GaussianBeam(w0, k)
        GaussianBeam((w0, z0), k)
        """
        self._z0 = 0.0
        if isinstance(w0z0, tuple):
            if len(w0z0)==1:
                self._w0 = w0z0[0]
            elif len(w0z0)==2:
                self._w0 = w0z0[0]
                self._z0 = w0z0[1]
            else:
                raise TypeError('Expecting a scalar or 2-element tuple.')
        else:
            try:
                w0z0 = float(w0z0)
                if isinstance(w0z0, float):
                    self._w0 = w0z0
            except:
                raise TypeError('Expecting a scalar or 2-element tuple.')
            
        self._k = k
        self._zc = confocalDistance(self._w0, k)
    
    def field(self, r, z):
        q = complexBeamParameter(self._zc, z - self._z0)
        A = fieldAmplitude(q, self._k, r)
        P = fieldPhase(q, self._k, r)
        # TODO: improve efficiency by calculating A and P from private members
        return A*np.exp(P*1j)
        

def confocalDistance(w0, k):
    """
    Confocal distance ZC [d] from beam waist radius W0 [d] and wave number K [1/d]
    
    See also: complexBeamParameter, beamRadius
    """
    return (0.5*k)*w0**2

def complexBeamParameter(zc, z):
    """
    Complex beam parameter Q [d] from confocal distance ZC [d] and position Z
    [d] along propagation direction.
    
    See also: confocalDistance
    """
    z = np.array(z)
    tmp1 = pl.zeros(z.shape, np.complex)
    tmp1.real = z
    zc = np.array(zc)
    tmp2 = pl.zeros(zc.shape, np.complex)
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
            R = np.inf
        else:
            R = 1.0/invq.real
    else:
        R = pl.zeros(q.shape, np.double)
        R[idx] = np.inf
        idx = ~idx
        R[idx] = 1.0/invq[idx].real;
    return R

def beamRadius(q, k):
    """
    Beam radius W [d] from complex beam parameter Q [d] and wave number K [1/d]
    
    See also: complexBeamParameter
    """
    lam = 2.0*np.pi/k;
    invq = 1.0/q;
    w = np.sqrt(lam/(-np.pi*invq.imag))
    return w

def beamWaistRadius(q, k):
    """
    Beam waist radius W0 [d] from complex beam parameter Q [d] and wave number K
    [1/d].
    
    See also: complexBeamParameter, beamWaistPosition
    """
    zc = q.imag
    w0 = np.sqrt(2*zc/k)
    return w0

def beamWaistPosition(q):
    """
    Beam waist position Z0 [d] from complex beam parameter Q [d] and wave number K
    [1/d].
    
    See also: complexBeamParameter, beamWaistRadius
    """
    z = q.real
    return -z

def beamWaist(q, k):
    """
    Beam waist radius, position as tuple (W0, Z0) [d] from complex beam
    parameter Q [d] and wave number K [1/d].
    
    See also: complexBeamParameter, beamWaistRadius, beamWaistPosition
    """
    zc = q.imag
    w0 = np.sqrt(2*zc/k)
    z = q.real
    return (w0, -z)

def fieldAmplitude(q, k, r):
    """
    Scalar field amplitude A relative to beam waist center from complex beam
    parameter Q [d], wave number K [1/d], at radial distance R [d] from the
    propagation axis.
    
    See P.F. Goldsmith, "Quasioptical Systems", Section 2.1, p.15
    
    See also: complexBeamParameter, beamRadius, fieldPhase
    """
    w = beamRadius(q, k)
    w0 = beamWaistRadius(q, k)
    A = w0/w*np.exp(-r**2/w**2)
    return A

def fieldPhase(q, k, r):
    """
    Field phase P [rad] referred to beam waist, at radial distance R [d] from
    the propagation axis.

    See P.F. Goldsmith, "Quasioptical Systems", Section 2.1, p.15
    
    See also: complexBeamParameter, radiusOfCurvature, fieldAmplitude
    """
    R = radiusOfCurvature(q)
    P = -0.5*k*r**2/R
    z = q.real
    zc = q.imag
    P0 = -k*z + np.arctan(z/zc)
    # TODO: sign of result assumes jwt time convention
    return np.mod(P + P0, 2*np.pi)
    
def test(dryTest=True):
    dryTest = bool(dryTest)
    pi = np.pi
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
    assert R == np.inf
    w = beamRadius(q, 2*pi/lam)
    assert abs(w-w0) < 1.0e-15
    print "Pass"
    print "Running array tests ..."
    w0 = 8.0
    lam = 3.0
    zc = confocalDistance(w0, 2*pi/lam)
    assert zc == pi*w0**2/lam
    z = np.array([0, zc])
    q = complexBeamParameter(zc, z)
    assert q.real[0]==z[0]
    assert q.real[1]==zc
    assert q.imag[0]==zc
    assert q.imag[1]==zc
    R = radiusOfCurvature(q)
    assert R[0] == np.inf
    assert R[1] == 2*zc
    w = beamRadius(q, 2*pi/lam)
    assert abs(w[0]-w0) < 1.0e-15
    assert abs(w[1]-np.sqrt(2.0)*w0) < 1.0e-12
    assert (beamWaistRadius(q[1], 2*pi/lam) - w0) < 1.0e-15
    if not dryTest: pl.figure(); pl.plot(z, w)
    print "Running field tests ..."
    r = np.array([0, w0, 2*w0])
    A = fieldAmplitude(q[0], 2*pi/lam, r)
    assert abs(A[0]-1) < 1.0e-15
    assert abs(A[1]-np.exp(-1.0)) < 1.0e-15
    assert abs(A[2]-np.exp(-4.0)) < 1.0e-15
    P = fieldPhase(q[0], 2*pi/lam, r)
    assert abs(P[0]) < 1.0e-15
    assert abs(P[1]) < 1.0e-15
    # TODO: add some characteristic points along Z
    print "Testing GaussianBeam class"
    gb = GaussianBeam(beamWaist(q[0], 2*pi/lam), 2*pi/lam)
    (R,Z)= pl.meshgrid(np.arange(-24,24), np.arange(0,100))
    if not dryTest: pl.figure(); pl.imshow(abs(gb.field(R, Z)))
    print "Pass"

# if __name__ == "__main__":

    
