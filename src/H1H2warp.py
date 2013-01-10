import numpy
import math

def H1H2warp(fundamental):
##    print fundamental
    U,S,Vh = numpy.linalg.svd(fundamental)
    V = Vh.T
##    print V
    if V[2,2] != 0: 
        e0 = V[:3,2] / V[2,2]
    else:
        V[2,2] = 0.0001
        e0 = V[:3,2] / V[2,2]
##    print e0
    a = -e0[1]
    b = e0[0]
    c = numpy.mat("0")
    d0 = numpy.bmat('a; b; c')
##    print d0

##    print U
    
    if U[2,2] != 0:
        e1 = U[:3,2] / U[2,2]
    else:
        U[2,2] = 0.0001
        e1 = U[:3,2] / U[2,2]
##    print e1


##    D,V = numpy.linalg.eig(fundamental)
####    print D
####    print V
##    e0 = V[:,0]
##    d0 = numpy.array([[-e0[1]],[e0[0]],[0]])
##    print V
##    print e0
##    print d0
##
##    D,V = numpy.linalg.eig(fundamental.T)
##    e1 = V[:,0]
####    print V
####    print e1

##    d0 = numpy.mat("1782; 16076; 0")
    print fundamental
    print d0

    Fd0 = fundamental * d0
    print Fd0
    Fd0[2] = Fd0[2]**2
    Fd0 = Fd0 / math.sqrt(Fd0.sum())
    print Fd0
##
##    d1 = numpy.array([-Fd0[1],Fd0[0],0])
##    print d1

H1H2warp(numpy.mat("0 0 -0.003; 0 0 -0.0023; 0.0002 0.0019 -0.0612"))
