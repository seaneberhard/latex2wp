import os
import unittest

from ..main import convert_one


def read(resource):
    resources = os.path.join(os.path.dirname(__file__), 'resources')
    with open(os.path.join(resources, resource)) as stream:
        return stream.read()


class TestLatexToWordPress(unittest.TestCase):
    def runTest(self):
        self.maxDiff = None
        tex = read('example.tex')
        html = convert_one(tex)
        html_expected = read('example.html')
        self.assertMultiLineEqual(html, html_expected)


class TestLatexBodyOnlyToWordPress(unittest.TestCase):
    def runTest(self):
        self.maxDiff = None
        tex = read('example.tex').split(r'\begin{document}')[1].split(r'\end{document}')[0]
        html = convert_one(tex)
        html_expected = read('example.html')
        self.assertMultiLineEqual(html, html_expected)


class TestLatexToStandardHtml(unittest.TestCase):
    def runTest(self):
        self.maxDiff = None
        tex = read('example.tex')
        html = convert_one(tex, html=True)
        html_expected = read('standard-html.html')
        self.assertMultiLineEqual(html, html_expected)


if __name__ == '__main__':
    unittest.main()
