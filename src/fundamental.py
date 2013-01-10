import numpy
import math

def fundamental(points0, points1):

    XY0, XY1 = formatForFund(points0, points1)
    T0_norm = normalizePoints(XY0)
    T1_norm = normalizePoints(XY1)
    X0_norm = numpy.dot(T0_norm, XY0)
    X1_norm = numpy.dot(T1_norm, XY1)
    A = calcA(X0_norm, X1_norm)
    Fundamental = calcFnorm(A, T0_norm, T1_norm)
    return Fundamental

def formatForFund(points0, points1):
    points0Trans = points0.T
    points1Trans = points1.T
##    print points0Trans
    ones = numpy.ones(points0.shape[0])
##    print numpy.array([ones])
    XY0 = numpy.append(points0Trans, numpy.array([ones]), 0)
##    print XY0
    
    XY1 = numpy.append(points1Trans, numpy.array([ones]), 0)

##    print XY1
    return XY0, XY1

def normalizePoints(points):
    pointsTrans = points.T
##    print pointsTrans
    s = sum(pointsTrans)
    x = s[0]/points.shape[0]
    y = s[1]/points.shape[0]
    z = s[2]/points.shape[0]
##    print s
##    print x
##    print y
##    print z

    xSub = numpy.dot(x,numpy.ones(pointsTrans.shape[0]))
    ySub = numpy.dot(y,numpy.ones(pointsTrans.shape[0]))
    zSub = numpy.dot(z,numpy.ones(pointsTrans.shape[0]))
    sub = numpy.array([xSub, ySub, zSub])
##    print pointsTrans
##    print sub.T
    normPoints = pointsTrans - sub.T
##    print normPoints
    d = numpy.array([1.])
    for i in range(normPoints.shape[0]):
        appendValue = numpy.array([normPoints[i,0]**2 + normPoints[i,1]])
        d = numpy.append(d, appendValue)
    d = numpy.delete(d, 0)
    Dm = math.sqrt(numpy.mean(d))
    sf = math.sqrt(2)/Dm

    for i in range(normPoints.shape[0]):
        normPoints[i,0] = normPoints[i,0]*sf
        normPoints[i,1] = normPoints[i,1]*sf
##    print normPoints


    T_norm = numpy.array([[sf, 0, -sf*x],[0, sf, -sf*y],[0, 0, 1]])
    return T_norm

def calcA(X0_norm, X1_norm):
    u1 = X0_norm[0,:].T
    v1 = X0_norm[1,:].T
    u2 = X1_norm[0,:].T
    v2 = X1_norm[1,:].T


    A = numpy.array([u2*u1, u2*v1, u2, v2*u1, v2*v1, v2, u1, v1, numpy.ones(u1.shape[0])])
    A = A.T
##    print A    
    return A

def calcFnorm(A, T0_norm, T1_norm):
    U, S, Vh = numpy.linalg.svd(A)
    
    V = Vh.T
##    print V
    Fvec = V[:,-1]
##    print Fvec
    F_norm = numpy.array([[Fvec[0], Fvec[1], Fvec[2]],[Fvec[3],Fvec[4],Fvec[5]],[Fvec[6],Fvec[7],Fvec[8]]])
##    print F_norm
    US, SS, VSh = numpy.linalg.svd(F_norm)
##    print SS
    SS[-1] = 0
    SS_Matrix = numpy.zeros((3,3), dtype = complex)
    SS_Matrix[:3,:3] = numpy.diag(SS)
##    print SS_Matrix
    F = numpy.dot(numpy.dot(US,SS_Matrix),VSh)
##    print F
    Fnorm = numpy.dot(numpy.dot(T1_norm.T,F),T0_norm)
##    print Fnorm
    return Fnorm



fundamental(numpy.array([[1771,1111],[2073.5,1056],[1963.5,1259.5],[1732.5,1435.5]]), numpy.array([[1771,1111],[2073.5,1056],[1963.5,1259.5],[1732.5,1435.5]]))
