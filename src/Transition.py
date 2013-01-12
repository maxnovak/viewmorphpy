import numpy
import math
def Transition(prewarp0, prewarp1, warpFeat0, warpFeat1, feat0, feat1):
####    #not implemented yet, could not understand alg without matlab
####    FeatureMorph(prewarp0, prewarp1, i, 10)
####    for i in range(10):
####        #might not need to use the X, might just use U because of not using
####        #matlab's Tform function
####        X = (1-i)*feat0 + i*feat1
####        
####        U = (1-i)*warpFeat0 + i*warpFeat1


        
def FeatureMorph():#im0, im1, i, N):
    #x,y
    #featuresPQ = numpy.mat([[1688,1340],[1508,1776],[2356,1380],[2280,1788],[1380,1880],[2344,1808],[1352,1312],[1844,1320]])
    P = numpy.mat([[1688,1340],[2356,1380],[1380,1880],[1352,1312]])
    Q = numpy.mat([[1508,1776],[2280,1788],[2344,1808],[1844,1320]])
    #featuresPQPrime = numpy.mat([[1344,1328],[1232,1784],[1860,1356],[1824,1792],[1124,1800],[1908,1808],[1700,1292],[2340,1332]])
    PP = numpy.mat([[1344,1328],[1860,1356],[1124,1800],[1700,1292]])
    QP = numpy.mat([[1232,1784],[1824,1792],[1908,1808],[2340,1332]])
    diffPQ = Q - P
    print diffPQ
    print P
    print Q
    maths = sum(numpy.power(diffPQ,2))
##    print maths
    normP = [[math.sqrt(maths[0,0])]]
    normQ = [[math.sqrt(maths[0,1])]]
    normPQ = numpy.bmat('normP normQ')
##    print normPQ
    normPQSq = multiply(normPQ, normPQ)
        
    
##FeatureMorph()
