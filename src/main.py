import numpy
import Image
import csv
from fundamental import *
from H1H2Calc import *
##from Transition import *
import cv

def main():
    image0 = Image.open('pic1.jpg')
    image1 = Image.open('pic2.jpg')
    #image[ y, x , rgb ]
    features0 = numpy.mat([[1771,1111],[2073.5,1056],[1963.5,1259.5],[1732.5,1435.5],[2095.5,1347.5],
                    [1908.5,1468.5],[1941.5,1666.5],[1210,1705],[2156,1551],[1534.5,2040.5],
                    [1952.5,1941.5],[1837,418],[1930.5,1100],[1611.5,1133],[2194.5,1039.5],
                    [1848,797.5],[2101,775.5],[1545.5,1408],[2167,1303.5]])
    features1 = numpy.mat([[1738,1111],[2117.5,1094.5],[1936,1309],[1710.5,1457.5],[2161.5,1430],
                    [1919.5,1512.5],[1925,1732.5],[1342,1633.5],[2420,1650],[1644.5,2029.5],
                    [2128.5,2035],[1941.5,374],[1936,1122],[1578.5,1111],[2288,1089],[1798.5,786.5],
                    [2095.5,803],[1540,1391.5],[2293.5,1364]])
    fund = fundamental(features0, features1)
    H1, H2 = H1H2Calc(fund)
    prewarp1, prewarp2 = WarpImages(image0, image1, H1, H2)
    features0, features1 = formatForFund(features0, features1)
    warpFeatures0 = WarpFeatures(features0.T, H1)
    warpFeatures1 = WarpFeatures(features1.T, H2)
    #Transition(prewarp1, prewarp2, warpFeatures0, warpFeatures1, features0, features1)
    Linear(prewarp1, prewarp2, H1, H2)    


def Linear(prewarp1, prewarp2, H1, H2):
    warp = cv.fromarray(numpy.zeros((500,500,3),numpy.uint8))
    for i in range(11):
        n = i/10.
        HS = (1-n)*H1 + n*H2
        HS = HS.T.copy()
        HS = cv.fromarray(HS)
        cv.AddWeighted(prewarp1, 1-n, prewarp2, n, 0.0, warp)
        cv.WarpPerspective(warp, warp, HS)
        cv.SaveImage("images/warp"+str(i)+".jpg", warp)


        
def WarpImages(image0, image1, H1, H2):
    imgarray0 = numpy.array(image0)
##    print imgarray0[0,0]
    imgarray1 = numpy.array(image1)
    cvimg1 = cv.fromarray(imgarray0)
##    print cvimg1[0,0]
    H1 = cv.fromarray(H1)
    cvimg2 = cv.fromarray(imgarray1)
    H2 = cv.fromarray(H2)
    out1 = cv.fromarray(numpy.zeros((500,500,3),numpy.uint8))
    out2 = cv.fromarray(numpy.zeros((500,500,3),numpy.uint8))
    cv.WarpPerspective(cvimg1, out1, H1)
    cv.WarpPerspective(cvimg2, out2, H2)
    
    cv.SaveImage("images/prewarp1.jpg", out1)
    cv.SaveImage("images/prewarp2.jpg", out2)
    return out1, out2

def  WarpFeatures(features, H):
    
    for row in features:
        row[:] = row[:] * H
    return features



if __name__ == "__main__":
    main()
