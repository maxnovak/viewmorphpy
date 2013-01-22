import numpy
import Image
import csv
from fundamental import *
from H1H2Calc import *
##from Transition import *
import cv
import profile

def main():
    image0 = cv.LoadImage('tests/grid.jpg')
    image1 = cv.LoadImage('tests/grid2.jpg')
    buff = cv.LoadImage('buff.jpg')
    buff2 = cv.LoadImage('buff.jpg')
    #image[ y, x , rgb ]
    features0 = []
    for row in csv.reader(open('tests/grid.csv')):
        features0.append([float(r) for r in row])
    features0 = numpy.mat(features0)
    features1 = []
    for row in csv.reader(open('tests/grid.csv')):
        features1.append([float(r) for r in row])
    features1 = numpy.mat(features1)
    
    fund = fundamental(features0, features1)
    H1, H2 = H1H2Calc(fund)
    prewarp1, prewarp2 = WarpImages(image0, image1, H1, H2, buff, buff2)
##    features0, features1 = formatForFund(features0, features1)
##    warpFeatures0 = WarpFeatures(features0.T, H1)
##    warpFeatures1 = WarpFeatures(features1.T, H2)
    #Transition(prewarp1, prewarp2, warpFeatures0, warpFeatures1, features0, features1)
    cv.NamedWindow('display')
##    cv.NamedWindow('prewarp1')
##    cv.NamedWindow('prewarp2')
    writer = cv.CreateVideoWriter("feed/out.avi", 0, 10, (1000,1000), True)
##    cv.ShowImage('prewarp1', prewarp1)
##    cv.WaitKey(0)
##    cv.ShowImage('prewarp2', prewarp2)
##    cv.WaitKey(0)
    Linear(prewarp1, prewarp2, H1, H2, writer)
    Linear(prewarp2, prewarp1, H2, H1, writer)
##    cv.ShowImage('prewarp1', prewarp1)
##    cv.WaitKey(0)
##    cv.ShowImage('prewarp2', prewarp2)
##    cv.WaitKey(0)
    


def Linear(img1, img2, H1, H2, writer):
    buff = cv.LoadImage('buff.jpg')
    for i in range(11):
        n = i/10.
        HS = (1-n)*H1 + (n)*H2
        HS = HS.T.copy()
        HS = cv.fromarray(HS)
        cv.AddWeighted(img1, 1-n, img2, n, 0.0, buff)
        cv.WarpPerspective(buff, buff, HS)
        cv.WriteFrame(writer, buff)
        cv.ShowImage('display', buff)
        cv.WaitKey(100)

        
        


        
def WarpImages(image0, image1, H1, H2,buff,buff2):
##    print imgarray0[0,0]
##    print cvimg1[0,0]
    H1 = cv.fromarray(H1)
    H2 = cv.fromarray(H2)
##    out1 = cv.fromarray(numpy.zeros((500,500,3),numpy.uint8))
##    out2 = cv.fromarray(numpy.zeros((500,500,3),numpy.uint8))
    cv.WarpPerspective(image0, buff, H1)
    cv.WarpPerspective(image1, buff2, H2)
    
    cv.SaveImage("images/prewarp1.jpg", buff)
    cv.SaveImage("images/prewarp2.jpg", buff2)
##    cv.NamedWindow('display')
##    cv.ShowImage('display', out1)
##    cv.WaitKey(0)
##    cv.ShowImage('display', out2)
##    cv.WaitKey(0)
    return buff, buff2

def  WarpFeatures(features, H):
    
    for row in features:
        row[:] = row[:] * H
    return features



if __name__ == "__main__":
    main()
##    cv.WaitKey(0)
    cv.DestroyWindow('display')
    cv.DestroyWindow('prewarp1')
    cv.DestroyWindow('prewarp2')
##    profile.run('main(); print')
