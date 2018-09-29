import os
import unittest

from .. import main


class TestConvert(unittest.TestCase):
    def setUp(self):
        resources = os.path.join(os.path.dirname(__file__), 'resources')

        def read(resource):
            with open(os.path.join(resources, resource)) as stream:
                return stream.read()

        self.tex = read('example.tex')
        self.tex_body_only = read('example-body-only.tex')
        self.html_expected = read('example.html')
        self.maxDiff = None

    def test_example(self):
        html = main.convert_one(self.tex)
        self.assertMultiLineEqual(html, self.html_expected)

    def test_example_body_only(self):
        import imp
        imp.reload(main)  # todo: remove this -- requires better containing the counters to local scopes
        html = main.convert_one(self.tex_body_only)
        self.assertMultiLineEqual(html, self.html_expected)


if __name__ == '__main__':
    unittest.main()
