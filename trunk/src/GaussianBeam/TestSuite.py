#!/usr/bin/env python
import unittest
import numpy as np

try:
    reload(GaussianBeam)
except:
    pass

from GaussianBeam import *

class GaussianBeamTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testFunScalarArgs(self):
        w0 = 8.0
        lam = 3.0
        k = 2*np.pi/lam
        zc = confocalDistance(w0, k)
        self.assertEqual(zc, np.pi*w0**2/lam)
        z = 0.0;
        q = complexBeamParameter(zc, z)
        self.assertEqual(q.real, z)
        self.assertEqual(q.imag, zc)
        R = radiusOfCurvature(q)
        self.assertEqual(R, np.inf)
        w = beamRadius(q, k)
        self.assertAlmostEqual(w, w0)
    
    def testFunArrayArgs(self):
        w0 = 8.0
        lam = 3.0
        k = 2*np.pi/lam
        zc = confocalDistance(w0, k)
        z = np.array([0, zc])
        q = complexBeamParameter(zc, z)
        self.assertEqual(q.real[0], z[0])
        self.assertEqual(q.real[1], zc)
        self.assertEqual(q.imag[0], zc)
        self.assertEqual(q.imag[1], zc)
        R = radiusOfCurvature(q)
        self.assertEqual(R[0], np.inf)
        self.assertEqual(R[1], 2*zc)
        w = beamRadius(q, k)
        self.assertAlmostEqual(w[0], w0)
        self.assertAlmostEqual(w[1], np.sqrt(2.0)*w0)
        self.assertAlmostEqual(beamWaistRadius(q[1], k), w0)
    
    #if not dryTest: pl.figure(); pl.plot(z, w)
    #print "Running field tests ..."
    #r = np.array([0, w0, 2*w0])
    #A = fieldAmplitude(q[0], 2*pi/lam, r)
    #assert abs(A[0]-1) < 1.0e-15
    #assert abs(A[1]-np.exp(-1.0)) < 1.0e-15
    #assert abs(A[2]-np.exp(-4.0)) < 1.0e-15
    #P = fieldPhase(q[0], 2*pi/lam, r)
    #assert abs(P[0]) < 1.0e-15
    #assert abs(P[1]) < 1.0e-15
    ## TODO: add some characteristic points along Z
    #print "Testing GaussianBeam class"
    #gb = GaussianBeam(beamWaist(q[0], 2*pi/lam), 2*pi/lam)
    #(R,Z)= pl.meshgrid(np.arange(-24,24), np.arange(0,100))
    #if not dryTest: pl.figure(); pl.imshow(abs(gb.field(R, Z)))
    #print "Testing ComplexBeamParameter class"
    #d = 10
    #q = gb.q(0)
    #abcd = np.matrix([[1, d],[0, 1]], dtype=float)
    #qo = abcd*q
    #assert qo == gb.q(d)
    #print "Testing ParaxialElement class"
    #el = ParaxialElement(abcd, 0)
    #gb2 = el*gb
    #print gb2.q(0)
    #print gb.q(d)
    #assert gb2.q(0)==gb.q(d)
    #print "Pass"
    
class ParaxialElementTest(unittest.TestCase):
    def setUp(self):
        self.gb = GaussianBeam((8.0, -50.0), 2*np.pi/3.0)
        
    def testThinLens(self):
        lens = ThinLens(150.0, 100.0)
        gbOut = lens*self.gb
        self.assertAlmostEqual(gbOut._z0, 250.0)
        M = lens.beamWaistMag(self.gb._zc, -50.0)
        self.assertAlmostEqual(gbOut._w0, self.gb._w0*M)
    
if __name__ == '__main__':
    #unittest.main()
    suiteGB = unittest.TestLoader().loadTestsFromTestCase(GaussianBeamTest)
    suitePE = unittest.TestLoader().loadTestsFromTestCase(ParaxialElementTest)
    suite = unittest.TestSuite([suiteGB, suitePE])
    unittest.TextTestRunner(descriptions=2, verbosity=2).run(suite)

    

