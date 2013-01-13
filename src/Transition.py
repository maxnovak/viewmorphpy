import numpy
import Image
import math
####def Transition(prewarp0, prewarp1, warpFeat0, warpFeat1, feat0, feat1):
####    #not implemented yet, could not understand alg without matlab
####    FeatureMorph(prewarp0, prewarp1, i, 10)
####    for i in range(10):
####        #might not need to use the X, might just use U because of not using
####        #matlab's Tform function
####        X = (1-i)*feat0 + i*feat1
####        
####        U = (1-i)*warpFeat0 + i*warpFeat1


        
def FeatureMorph(im0, im1, i):
    i = 0.5
    #x,y
    P = numpy.mat([[1688,1340],[2356,1380],[1380,1880],[1352,1312]])
    Q = numpy.mat([[1508,1776],[2280,1788],[2344,1808],[1844,1320]])
    PPrime = numpy.mat([[1344,1328],[1860,1356],[1124,1800],[1700,1292]])
    QPrime = numpy.mat([[1232,1784],[1824,1792],[1908,1808],[2340,1332]])
    Padd = (1-i)*P + i*PPrime
    Qadd = (1-i)*Q + i*QPrime
    diffPQdest = Qadd - Padd
    sumPQ = sum(numpy.power(diffPQdest,2).T).T
    normPQdest = numpy.mat([math.sqrt(row) for row in sumPQ]).T
    normPQdestsq = numpy.power(normPQdest,2)
    a = diffPQdest[:,1]
    b = -1*diffPQdest[:,0]
    perpPQdest = numpy.bmat('a b')
    diffPQsource = QPrime - PPrime
    sumPQPrime = sum(numpy.power(diffPQsource,2).T).T
    normPQsource = numpy.mat([math.sqrt(row) for row in sumPQPrime]).T
    a = diffPQsource[:,1]
    b = -1*diffPQdest[:,0]
    perpPQsource = numpy.bmat('a b')

    DSUM = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.uint8)
    Xsource = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.uint8)
    Xdest = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.uint8)
    XP = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.uint8)
    weightsum = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.uint8)

    X1 = numpy.ones((1,im0.shape[1]),numpy.uint8)
    X2 = numpy.mat(numpy.arange(1, im0.shape[0]+1, 1)).T
    Xsource[:,:,0] = X2 * X1
    Y1 = numpy.ones((im0.shape[0],1),numpy.uint8)
    Y2 = numpy.mat(numpy.arange(1, im0.shape[1]+1, 1))
    Xsource[:,:,1] = Y1 * Y2

    for k in range(4):
        XP[:,:,0] = Xsource[:,:,0] - Padd[k,0]
        XP[:,:,1] = Xsource[:,:,1] - Padd[k,1]

        u = (multiply(XP[:,:,0],diffPQdest[k,0]) + multiply(XP[:,:,1],diffPQdest[k,1])) / normPQdestsq[k,0]
        v = (multiply(XP[:,:,0],perpPQdest[k,0]) + multiply(XP[:,:,1],perpPQdest[k,2])) / normPQdest[k,0]
        
        Xdest[:,:,0] = PPrime(k,0,0) + multiply(u, diffPQsource[k,0]) + multiply(v,perpPQsource[k,0]) / normPQsource[k,0]
        Xdest[:,:,1] = PPrime(k,1,0) + multiply(u, diffPQsource[k,1]) + multiply(v,perpPQsource[k,1]) / normPQsource[k,0]

        D = Xdest - Xsource

        Xx = Xdest[:,:,0]
        Xy = Xdest[:,:,1]

        dist = 
        
                

if __name__ == "__main__":
                image0 = Image.open('pic1.jpg')
                image0 = numpy.array(image0)
                image1 = Image.open('pic2.jpg')
                image1 = numpy.array(image1)
                FeatureMorph(image0, image1, 0.5)
