"""
 Original work: Copyright 2009 Luca Trevisan
 (additional contributors: Radu Grigore)

 Modified work: Copyright 2018 Sean Eberhard
 (additional contributors: see https://github.com/seaneberhard/latex2wp/graphs/contributors)

 This file is part of LaTeX2WP, a program that converts
 a LaTeX document into a format that is ready to be
 copied and pasted into WordPress.

 You are free to redistribute and/or modify LaTeX2WP under the
 terms of the GNU General Public License (GPL), version 3
 or (at your option) any later version.

 I hope you will find LaTeX2WP useful, but be advised that
 it comes WITHOUT ANY WARRANTY; without even the implied warranty
 of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GPL for more details.

 You should have received a copy of the GNU General Public
 License along with LaTeX2WP.  If you can't find it,
 see <http://www.gnu.org/licenses/>.
"""

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
