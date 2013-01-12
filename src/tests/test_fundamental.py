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

        expected = numpy.array([[  3.01805937e-08, 9.93241494e-08, -3.08139862e-04],
                                [  1.40534854e-07, 1.58636530e-09, -2.25634230e-03],
                                [  2.19215677e-04, 1.94282659e-03, -6.12417916e-02]])
        assert(numpy.allclose(expected, fundamental.fundamental(self.img0.features, self.img1.features)))


