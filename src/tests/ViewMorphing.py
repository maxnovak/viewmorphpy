'''uses PIL 1.1.7 and numpy-1.6.2'''

import Image
import numpy
import csv


def Main():
    image0 = Image.open("pic1.jpg")
    image1 = Image.open("pic2.jpg")

    aImage0 = numpy.array(image0)
    aImage1 = numpy.array(image1)

    file1 = open('pic1.csv')
    
    reader = csv.reader(file1,delimiter=',')
    for row in reader:
        print '\t'.join(row)


Main()
