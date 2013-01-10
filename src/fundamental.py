import numpy
import math

def fundamental(points0, points1):

    XY0, XY1 = formatForFund(points0, points1)
    T0_norm = normalizePoints(XY0)
    T1_norm = normalizePoints(XY1)
    X0_norm = T0_norm * XY0
    X1_norm = T1_norm * XY1
    A = calcA(X0_norm, X1_norm)
    Fundamental = calcFnorm(A, T0_norm, T1_norm)
##    print Fundamental
    return Fundamental

def formatForFund(points0, points1):
    points0Trans = points0.T
    points1Trans = points1.T
##    print points0Trans
    ones = numpy.ones(points0.shape[0])
##    print numpy.array([ones])
    XY0 = numpy.append(points0Trans, numpy.mat([ones]), 0)
##    print XY0
    
    XY1 = numpy.append(points1Trans, numpy.mat([ones]), 0)

##    print XY1
    return XY0, XY1

def normalizePoints(points):
    pointsTrans = points.T
##    print pointsTrans
    s = sum(pointsTrans)
    x = s[0,0]/points.shape[0]
    y = s[0,1]/points.shape[0]
    z = s[0,2]/points.shape[0]
##    print s
##    print x
##    print y
##    print z

    xSub = x * numpy.ones(pointsTrans.shape[0])
    ySub = y * numpy.ones(pointsTrans.shape[0])
    zSub = z * numpy.ones(pointsTrans.shape[0])
    sub = numpy.mat([xSub, ySub, zSub])
##    print pointsTrans
##    print sub.T
    normPoints = pointsTrans - sub.T
##    print normPoints
    d = numpy.array([1.])
    for i in range(normPoints.shape[0]):
        appendValue = numpy.mat([normPoints[i,0]**2 + normPoints[i,1]])
        d = numpy.append(d, appendValue)
    d = numpy.delete(d, 0)
    Dm = math.sqrt(numpy.mean(d))
    sf = math.sqrt(2)/Dm

    for i in range(normPoints.shape[0]):
        normPoints[i,0] = normPoints[i,0]*sf
        normPoints[i,1] = normPoints[i,1]*sf
##    print normPoints


    T_norm = numpy.mat([[sf, 0, -sf*x],[0, sf, -sf*y],[0, 0, 1]])
    return T_norm

def calcA(X0_norm, X1_norm):
    u1 = X0_norm[0,:].T
    v1 = X0_norm[1,:].T
    u2 = X1_norm[0,:].T
    v2 = X1_norm[1,:].T
    a = numpy.multiply(u2,u1)
    b = numpy.multiply(u2,v1)
    c = numpy.multiply(v2,u1)
    d = numpy.multiply(v2,v1)
    e = numpy.mat(numpy.ones(u1.shape[0])).T
##    print a
##    print b
##    print c
##    print d
##    print e
##    print u2
##    print v2
##    print u1
##    print v1
    
    A = numpy.bmat('a b u2 c d v2 u1 v1 e')

##    print A    
    return A

def calcFnorm(A, T0_norm, T1_norm):
    U, S, Vh = numpy.linalg.svd(A)
    
    V = Vh.T
##    print V
    Fvec = V[:,-1]
##    print Fvec
    Fvec = Fvec.T
    F_norm = numpy.mat([[Fvec[0,0], Fvec[0,1], Fvec[0,2]],[Fvec[0,3],Fvec[0,4],Fvec[0,5]],[Fvec[0,6],Fvec[0,7],Fvec[0,8]]])
##    print F_norm
    US, SS, VSh = numpy.linalg.svd(F_norm)
##    print SS
    SS[-1] = 0
    SS_Matrix = numpy.zeros((3,3), dtype = complex)
    SS_Matrix[:3,:3] = numpy.diag(SS)
##    print SS_Matrix
    F = US * SS_Matrix * VSh
##    print F
    Fnorm = T1_norm.T * F * T0_norm
##    print Fnorm 
    return Fnorm



#fundamental(numpy.mat([[1771,1111],[2073.5,1056],[1963.5,1259.5],[1732.5,1435.5],[2095.5,1347.5],[1908.5,1468.5],[1941.5,1666.5],[1210,1705],[2156,1551]]), numpy.mat([[1738,1111],[2117.5,1094.5],[1936,1309],[1710.5,1457.5],[2161.5,1430],[1919.5,1512.5],[1925,1732.5],[1342,1633.5],[2420,1650]]))
