import numpy
import math
from fundamental import *

def H1H2Calc(fundamental):
    e0,d0,e1,d1 = FindEAndD(fundamental)
    dividend = d0[1]*e0[0] - d0[0]*e0[1]
    
    theta0 = numpy.arctan(e0[2]/dividend[0])
    dividend = d1[1]*e1[0] - d1[0]*e1[1]
    theta1 = numpy.arctan(e1[2]/dividend[0])
    rdt0 = Rotation(d0, theta0)
    rdt0n = Rotation(d0,-theta0)
    rdt1 = Rotation(d1,theta1)

    erdt0 = rdt0*e0
    erdt1 = rdt1*e1
    phi0 = -numpy.arctan(erdt0[1]/erdt0[0])
    phi1 = -numpy.arctan(erdt1[1]/erdt1[0])

    rp0 = RotationPhi(phi0)
    rp0n = RotationPhi(-phi0)
    rp1 = RotationPhi(phi1)
    FR = rp1 * rdt1 * fundamental * rdt0n * rp0n
##    print FR
    
    T = CalcT(FR)

    H1 = rp0 * rdt0
    H2 = T * rp1 * rdt1
    print "Warp Matrix for image 1:\n", H1
    print "Warp Matrix for image 2:\n", H2
    return H1,H2

def CalcT(FR):
##    print FR[2,1]
    FR = FR / FR[2,1]
##    print FR
    a = numpy.mat("1")
    b = numpy.mat("0")
    c = numpy.mat(-FR[1,2])
    d = numpy.mat(-FR[2,2])
##    print a
##    print b
##    print c
##    print d
    
    
    T = numpy.bmat('a b b; b c d; b b a')
    return T

    
def Rotation(d, theta):
    cs = numpy.cos(theta)
    s = numpy.sin(theta)
    t = 1 - numpy.cos(theta)
    x = d[0]
    y = d[1]

    a = x*x+(1-x*x)*cs
    b = x*y*t
    c = y*s
    d = x*y*t
    e = y*y+(1-y*y)*cs
    f = -x*s
    g = -y*s
    h = x*s
    i = cs
    R = numpy.bmat('a b c; d e f; g h i')
##    print R
    return R

def RotationPhi(phi):
    a = numpy.cos(phi)
    b = -numpy.sin(phi)
    c = numpy.mat("0")
    d = numpy.sin(phi)
    e = numpy.mat("1")
    
    R = numpy.bmat('a b c; d a c; c c e')
##    print R
    return R

def FindEAndD(fundamental):
##    print fundamental
    U,S,Vh = numpy.linalg.svd(fundamental)
    V = Vh.T
##    print U
##    print S
##    print V
    e0 = V[:,2] / V[2,2]
    
##    print e0
    
    a = -e0[1] 
    b = e0[0]
    c = numpy.mat("0")
    d0 = numpy.bmat('a; b; c')
##    print d0

##    print U
    
    e1 = U[:3,2] / U[2,2]
##    print e1

####''' Alternate method in matlab, not using'''
##    
##    D,V = numpy.linalg.eig(fundamental)
####    print D
####    print V
##    e0 = V[:,0]
##    a = -e0[1]
##    b = e0[0]
##    c = numpy.mat("0")
##    d0 = numpy.bmat('a; b; c')
##    print V
##    print e0
##    print d0
##
##    D,V = numpy.linalg.eig(fundamental.T)
##    e1 = V[:,0]
####    print V
##    print e1



    Fd0 = fundamental * d0
##    print Fd0
    Fd0[2] = Fd0[2]**2
    Fd0 = Fd0 / math.sqrt(Fd0.sum())
##    print Fd0
    a = -Fd0[1]
    b = Fd0[0]
    c = numpy.mat("0")
    d1 = numpy.bmat('a;b;c')
##    print d1

    return e0, d0, e1, d1


if __name__ == "__main__":
    fund = fundamental(numpy.mat([[1771,1111],[2073.5,1056],[1963.5,1259.5],[1732.5,1435.5],[2095.5,1347.5],
                              [1908.5,1468.5],[1941.5,1666.5],[1210,1705],[2156,1551],[1534.5,2040.5],
                              [1952.5,1941.5],[1837,418],[1930.5,1100],[1611.5,1133],[2194.5,1039.5],
                              [1848,797.5],[2101,775.5],[1545.5,1408],[2167,1303.5]]),
                   numpy.mat([[1738,1111],[2117.5,1094.5],[1936,1309],[1710.5,1457.5],[2161.5,1430],
                              [1919.5,1512.5],[1925,1732.5],[1342,1633.5],[2420,1650],[1644.5,2029.5],
                              [2128.5,2035],[1941.5,374],[1936,1122],[1578.5,1111],[2288,1089],[1798.5,786.5]
                              ,[2095.5,803],[1540,1391.5],[2293.5,1364]]))
    H1H2Calc(fund)
