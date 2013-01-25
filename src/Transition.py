import numpy
import Image
import math
import profile
####def Transition(prewarp0, prewarp1, warpFeat0, warpFeat1, feat0, feat1):
####    #not implemented yet, could not understand alg without matlab
####    FeatureMorph(prewarp0, prewarp1, i, 10)
####    for i in range(10):
####        #might not need to use the X, might just use U because of not using
####        #matlab's Tform function
####        X = (1-i)*feat0 + i*feat1
####        
####        U = (1-i)*warpFeat0 + i*warpFeat1


        
def FeatureMorph(im0, im1, i, N):
    
    #x,y
    #imageLine(:,:,1) = P
    #imageLine(:,:,2) = Q
    #imageLine(:,:,3) = P'
    #imageLine(:,:,4) = Q'
    #imageLine(:,:,5) = PAdd
    #imageLine(:,:,6) = QAdd
    P = numpy.mat([[155,238],[157,234],[169,308],[170,252],[210,219],[212,300],[85,273],[86,280],[216,194],[236,283]])
    Q = numpy.mat([[150,302],[209,216],[210,299],[170,293],[230,266],[230,267],[133,267],[128,300],[282,198],[278,268]])
    PPrime = numpy.mat([[178,235],[177,235],[204,316],[198,249],[243,218],[260,309],[99,283],[99,286],[261,210],[279,304]])
    QPrime = numpy.mat([[182,305],[242,215],[258,309],[201,295],[275,263],[278,265],[152,261],[158,297],[327,214],[332,285]])
    Padd = (1-i)*P + i*PPrime
    Qadd = (1-i)*Q + i*QPrime
    diffPQdest = Qadd - Padd
    sumPQ = sum(numpy.power(diffPQdest,2).T).T
    normPQdest = numpy.mat([math.sqrt(row) for row in sumPQ]).T
    normPQdestsq = numpy.power(normPQdest,2)
    a = diffPQdest[:,1]
    b = -1*diffPQdest[:,0]
    perpPQdest = numpy.bmat('a b')
    diffPQsource = Q - P
    sumPQ = sum(numpy.power(diffPQsource,2).T).T
    normPQsource = numpy.mat([math.sqrt(row) for row in sumPQ]).T
    a = diffPQsource[:,1]
    b = -1*diffPQsource[:,0]
    perpPQsource = numpy.bmat('a b')

    DSUM = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.float)
    Xsource = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.float)
    Xdest = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.float)
    XP = numpy.zeros((im0.shape[0],im0.shape[1],2),numpy.float)
    weightsum = numpy.zeros((im0.shape[0],im0.shape[1]),numpy.float)

    X1 = numpy.ones((1,im0.shape[1]),numpy.float)
    X2 = numpy.mat(numpy.arange(1, im0.shape[0]+1, 1)).T
    Xsource[:,:,0] = X2 * X1
    Y1 = numpy.ones((im0.shape[0],1),numpy.float)
    Y2 = numpy.mat(numpy.arange(1, im0.shape[1]+1, 1))
    Xsource[:,:,1] = Y1 * Y2



    for k in range(N):
        XP[:,:,0] = Xsource[:,:,0] - Padd[k,0]
        XP[:,:,1] = Xsource[:,:,1] - Padd[k,1]

        u = (numpy.multiply(XP[:,:,0],diffPQdest[k,0]) + numpy.multiply(XP[:,:,1],diffPQdest[k,1])) / normPQdestsq[k,0]
        v = (numpy.multiply(XP[:,:,0],perpPQdest[k,0]) + numpy.multiply(XP[:,:,1],perpPQdest[k,1])) / normPQdest[k,0]

        vtemp = numpy.ones((v.shape[0],v.shape[1]),numpy.float)
        for row in range(v.shape[0]):
            for col in range(v.shape[1]):
                vtemp[row, col] = abs(v[row,col])

        
        Xdest[:,:,0] = P[k,0] + numpy.multiply(u, diffPQsource[k,0]) + numpy.multiply(v,perpPQsource[k,0]) / normPQsource[k,0]
        Xdest[:,:,1] = P[k,1] + numpy.multiply(u, diffPQsource[k,1]) + numpy.multiply(v,perpPQsource[k,1]) / normPQsource[k,0]
        D = Xdest - Xsource

        Xx = Xdest[:,:,0]
        Xy = Xdest[:,:,1]

        dist = vtemp
        I = numpy.nonzero(u > 1)


        temp = numpy.power((Xx[I] - Qadd[k,0]),2) + numpy.power((Xy[I] - Qadd[k,1]),2)
        dist[I] = [math.sqrt(item) for item in temp]
        
        
        I = numpy.nonzero(u < 0)
##        print I
        temp = numpy.power((Xx[I] - Padd[k,0]),2) + numpy.power((Xy[I] - Padd[k,1]),2)      
        dist[I] = [math.sqrt(item) for item in temp]
        
        weight = numpy.power((numpy.power(normPQdest[k],0.4)/(2 + dist)),2)
        DSUM[:,:,0] = DSUM[:,:,0] + numpy.multiply(D[:,:,0],weight)
        DSUM[:,:,1] = DSUM[:,:,1] + numpy.multiply(D[:,:,1],weight)
        
        weightsum = weightsum + weight

    Xxs = numpy.zeros((numpy.shape(DSUM)),numpy.float)
    
    Xxs[:,:,0] = Xsource[:,:,0] + DSUM[:,:,0] / weightsum
    Xxs[:,:,1] = Xsource[:,:,1] + DSUM[:,:,1] / weightsum

    x0 = image0.shape[0]
    y0 = image0.shape[1]

    premorph0 = numpy.zeros(numpy.shape(image0))

    Xxs0 = Xxs[:,:,0]
    Xxs1 = Xxs[:,:,1]

    yes = numpy.nonzero((Xxs0 > 0) & (Xxs0 <= x0) & (Xxs1 > 0) & (Xxs1 <= y0))
    print yes
    #stores as two arrays, x and y values in each array

##    test = Xxs0[yes] + (Xxs1[yes]-1)*x0
##    temp = numpy.nonzero(test > 0)
    
    image0a = image0[:]
    premorph0a = numpy.zeros(numpy.shape(image0))
    print numpy.shape(Xxs0[yes])
    print numpy.shape(Xxs1[yes]-1)
    
##    current issue is with getting indexed values for image0a from the values retrived from Xxs0 with the "yes" indexes
##    print (Xxs0[yes] + (Xxs1[yes]-1)*x0) # proving that the stuff within image0a in the line below is actual values and not indexes
    premorph0a[yes] = image0a[(Xxs0[yes] + (Xxs1[yes]-1)*x0)]
    premorph0a[x0*y0 + yes] = image0[x0*y0 + (Xxs0[yes] + (Xxs1[yes]-1)*x0)]
    premorph0a[2*x0*y0 + yes] = image0[2*x0*y0 + (Xxs0[yes] + (Xxs1[yes] - 1) * x0)]
    premorph0 = numpy.reshape(premorph0a, (x0,y0,3))
    
#################################
    diffPQsource = QPrime - PPrime
    sumPQ = sum(numpy.power(diffPQdest,2).T).T
    normPQsource = numpy.mat([math.sqrt(row) for row in sumPQ]).T
    a = diffPQsource[:,1]
    b = -1*diffPQdest[:,0]
    perpPQsource = numpy.bmat('a b')
    print numpy.shape(image0)
    DSUM = numpy.zeros((image0.shape[0], image0.shape[1], 2), numpy.float)
    D = numpy.zeros(numpy.shape(DSUM), numpy.float)
    Xdest = numpy.zeros(numpy.shape(DSUM), numpy.float)
    XP = numpy.zeros(numpy.shape(DSUM), numpy.float)
    weightsum = numpy.zeros((image0.shape[0], image0.shape[1]), numpy.float)

    for k in range(N):
        XP[:,:,0] = Xsource[:,:,0] - Padd[k,0]
        XP[:,:,1] = Xsource[:,:,1] - Padd[k,1]

        u = (numpy.multiply(XP[:,:,0],diffPQdest[k,0]) + numpy.multiply(XP[:,:,1],diffPQdest[k,1])) / normPQdestsq[k,0]
        v = (numpy.multiply(XP[:,:,0],perpPQdest[k,0]) + numpy.multiply(XP[:,:,1],perpPQdest[k,1])) / normPQdest[k,0]
        vtemp = numpy.ones((v.shape[0],v.shape[1]),numpy.float)
        for row in range(v.shape[0]):
            for col in range(v.shape[1]):
                vtemp[row, col] = abs(v[row,col])

        
        Xdest[:,:,0] = PPrime[k,0] + numpy.multiply(u, diffPQsource[k,0]) + numpy.multiply(v,perpPQsource[k,0]) / normPQsource[k,0]
        Xdest[:,:,1] = PPrime[k,1] + numpy.multiply(u, diffPQsource[k,1]) + numpy.multiply(v,perpPQsource[k,1]) / normPQsource[k,0]

        D = Xdest - Xsource

        Xx = Xdest[:,:,0]
        Xy = Xdest[:,:,1]

        dist = vtemp
        I = numpy.nonzero(u > 1)

        temp = numpy.power((Xx[I] - Qadd[k,0]),2) + numpy.power((Xy[I] - Qadd[k,1]),2)
        dist[I] = [math.sqrt(item) for item in temp]
        
        
        I = numpy.nonzero(u < 0)
        temp = numpy.power((Xx[I] - Padd[k,0]),2) + numpy.power((Xy[I] - Padd[k,1]),2)      
        dist[I] = [math.sqrt(item) for item in temp]
        
        weight = numpy.power((numpy.power(normPQdest[k],0.4)/(2 + dist)),2)
        DSUM[:,:,0] = DSUM[:,:,0] + numpy.multiply(D[:,:,0],weight)
        DSUM[:,:,1] = DSUM[:,:,1] + numpy.multiply(D[:,:,1],weight)
        
        weightsum = weightsum + weight

    Xxs = numpy.zeros(numpy.shape(DSUM))
    Xxs[:,:,0] = Xsource[:,:,0] + DSUM[:,:,0] / weightsum
    Xxs[:,:,1] = Xsource[:,:,1] + DSUM[:,:,1] / weightsum

    x0 = image0.shape[0]
    y0 = image0.shape[1]

    premorph0 = numpy.zeros(numpy.shape(image0))

    Xxs0 = Xxs[:,:,0]
    Xxs1 = Xxs[:,:,1]

##    yes = numpy.nonzero((Xxs0 > 0) & (Xxs0 <= x0) & (Xxs1 > 0) & (Xxs <= y0))

    yes = numpy.nonzero(Xxs0 > 0) 
    print yes
    premorph1a = numpy.zeros(numpy.shape(image0))
    premorph1a[yes] = image0[Xxs0[yes] + (Xxs1[yes]-1)*x0]
    premorph1a[x0*y0 + yes] = image0[x0*y0 + (Xxs0[yes] + (Xxs[yes]-1)*x0)]
    premorph1a[2*x0*y0 + yes] = image0[2*x0*y0 + (Xxs0[yes] + (Xxs1[yes] - 1))]
    premorph1 = numpy.reshape(premorph1a, (x0,y0,3))

    morphImage = (1-i) * premorph0 + (i) * premorph1
    

if __name__ == "__main__":
    image0 = Image.open('pic1.jpg')
    image0 = numpy.array(image0)
    image1 = Image.open('pic2.jpg')
    image1 = numpy.array(image1)
    FeatureMorph(image0, image1, 1, 10)
