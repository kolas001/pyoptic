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

def fieldAmplitude(w0, k, z, r):
    """
    Scalar field amplitude A relative to beam waist center from beam waist W0
    [d], wave number K [1/d], at position (R, Z) [d], where R is distance
    from propagation axis Z.
    
    See P.F. Goldsmith, "Quasioptical Systems", Section 2.1, p.15
    
    See also: confocalDistance, complexBeamParameter, beamRadius, fieldPhase
    """
    zc = confocalDistance(w0, k)
    q = complexBeamParameter(zc, z)
    w = beamRadius(q, k)
    A = w0/w*np.exp(-r**2/w**2)
    return A

def fieldPhase(w0, k, z, r):
    """
    Field phase P [rad] at transverse position R [d], measured from the phase
    center at beamwaist.

    See P.F. Goldsmith, "Quasioptical Systems", Section 2.1, p.15
    
    See also: confocalDistance, complexBeamParameter, radiusOfCurvature,
    fieldAmplitude
    """
    zc = confocalDistance(w0, k)
    q = complexBeamParameter(zc, z)
    R = radiusOfCurvature(q)
    P = -0.5*k*r**2/R    
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
    if not dryTest: pl.plot(z, w)
    print "Running field tests ..."
    r = np.array([0, w0, 2*w0])
    A = fieldAmplitude(w0, 2*pi/lam, 0, r)
    assert abs(A[0]-1) < 1.0e-15
    assert abs(A[1]-np.exp(-1.0)) < 1.0e-15
    assert abs(A[2]-np.exp(-4.0)) < 1.0e-15
    P = fieldPhase(w0, 2*pi/lam, 0, r)
    assert abs(P[0]) < 1.0e-15
    assert abs(P[1]) < 1.0e-15
    # TODO: add some characteristic points along Z
    print "Pass"

# if __name__ == "__main__":

    
