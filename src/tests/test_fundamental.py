import numpy
import csv
from collections import namedtuple
import Image


import fundamental

from nose.tools import assert_equal

ImageTuple = namedtuple("Image", ['array', 'features'])

class TestFundamental(object):

    def setup(self):
        self.img0 = self.load_image('src/tests/pic1.jpg', 'src/tests/pic1.csv')
        self.img1 = self.load_image('src/tests/pic2.jpg', 'src/tests/pic2.csv')

    def load_image(self, image_file, feature_file):
        image = Image.open(image_file)
        array = numpy.array(image)
        features = []
        for row in csv.reader(open(feature_file)):
            features.append([float(r) for r in row])

        return ImageTuple(array, numpy.mat(features))

    def test_image_array_shape(self):
        assert_equal((335, 500, 3), self.img0.array.shape)

    def test_fundamental(self):
        f = fundamental.fundamental(self.img0.features, self.img1.features)
        expected = numpy.array([[  4.51920950e-09+0.j, 6.38289111e-10+0.j, -1.26394050e-05+0.j],
                    [  1.89291668e-09+0.j, 1.09709829e-09+0.j, -9.60231967e-06+0.j],
                    [ -2.65578925e-06+0.j, 5.38727389e-06+0.j, -2.24914918e-02+0.j]])
        assert(numpy.allclose(expected, f))

