import os
import unittest

from .. import main


def read(resource):
    resources = os.path.join(os.path.dirname(__file__), 'resources')
    with open(os.path.join(resources, resource)) as stream:
        return stream.read()


def reload_main():
    # todo: remove this -- requires better containing the counters to local scopes
    import imp
    imp.reload(main)


class TestConvert(unittest.TestCase):
    def runTest(self):
        reload_main()
        self.maxDiff = None
        tex = read('example.tex')
        html = main.convert_one(tex)
        html_expected = read('example.html')
        self.assertMultiLineEqual(html, html_expected)


class TestConvertBodyOnly(unittest.TestCase):
    def runTest(self):
        reload_main()
        self.maxDiff = None
        tex = read('example-body-only.tex')
        html = main.convert_one(tex)
        html_expected = read('example.html')
        self.assertMultiLineEqual(html, html_expected)


class TestStandardHtml(unittest.TestCase):
    def runTest(self):
        reload_main()
        self.maxDiff = None
        tex = read('example.tex')
        html = main.convert_one(tex, standard_html=True)
        html_expected = read('standard-html.html')
        self.assertMultiLineEqual(html, html_expected)


if __name__ == '__main__':
    unittest.main()
