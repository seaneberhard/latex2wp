import os
import unittest

from .. import main


class TestConvert(unittest.TestCase):
    def setUp(self):
        resources = os.path.join(os.path.dirname(__file__), 'resources')
        with open(os.path.join(resources, 'example.tex')) as stream:
            self.tex = stream.read()
        with open(os.path.join(resources, 'example.html')) as stream:
            self.html_expected = stream.read()
        self.maxDiff = None

    def test_equals_exactly(self):
        html = main.convert_one(self.tex)
        self.assertMultiLineEqual(html, self.html_expected)


if __name__ == '__main__':
    unittest.main()
