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

# color of LaTeX formulas
textcolor = '000000'

# colors that can be used in the text
colors = dict(red='ff0000', green='00ff00', blue='0000ff')

# counters for theorem-like environments
# assign any counter to any environment. Make sure that
# maxcounter is an upper bound to the any counter being used
theorems = dict(theorem=0, lemma=0, proposition=0, definition=0, corollary=0, conjecture=0, remark=3, example=1,
                claim=4, exercise=2)

# the way \begin{theorem}, \begin{lemma} etc are translated in HTML
# the string _ThmType_ stands for the type of theorem
# the string _ThmNumb_ is the theorem number
beginthm = '\n<blockquote><b>_ThmType_ _ThmNumb_</b> <em>'

# translation of \begin{theorem}[...]. The string
# _ThmName_ stands for the content betwee the
# square brackets
beginnamedthm = '\n<blockquote><b>_ThmType_ _ThmNumb_ (_ThmName_)</b> <em>'

# translation of \end{theorem}, \end{lemma}, etc.
endthm = '</em></blockquote>\n<p>\n'

beginproof = '<em>Proof:</em> '


def endproof(html):
    if html:
        return r'<img src="http://l.wordpress.com/latex.php?latex=\Box&fg=000000">'
    return '$latex \Box&fg=000000$\n\n'


section = '\n<p>\n<b>_SecNumb_. _SecName_ </b>\n<p>\n'
sectionstar = '\n<p>\n<b> _SecName_ </b>\n<p>\n'
subsection = '\n<p>\n<b>  _SecNumb_._SubSecNumb_. _SecName_ </b>\n<p>\n'
subsectionstar = '\n<p>\n<b> _SecName_ </b>\n<p>\n'

# Font styles. Feel free to add others. The key *must* contain
# an open curly bracket. The value is the namem of a HTML tag.
fontstyle = {
    r'{\em ': 'em',
    r'{\bf ': 'b',
    r'{\it ': 'i',
    r'{\sl ': 'i',
    r'\textit{': 'i',
    r'\textsl{': 'i',
    r'\emph{': 'em',
    r'\textbf{': 'b',
}
