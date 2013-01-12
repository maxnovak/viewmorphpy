import numpy
import csv
from collections import namedtuple
import Image


from nose.tools import assert_equal

ImageTuple = namedtuple("Image", ['array', 'features'])

class TestFundamental(object):

    def setup(self):
        self.img0 = self.load_image('src/tests/pic1.jpg', 'src/tests/pic1.csv')
        self.img1 = self.load_image('src/tests/pic2.jpg', 'src/tests/pic2.csv')

    def load_image(self, image_file, feature_file):
        image = Image.open(image_file)
        array = numpy.array(image)
        features = csv.reader(open(feature_file))
        return ImageTuple(array, features)

    def test_image_array_shape(self):

        assert_equal((335, 500, 3), self.img0.array.shape)
