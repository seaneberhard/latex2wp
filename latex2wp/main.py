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

import re

from . import style


class ParseError(Exception):
    """base exception for all parse errors"""
    pass


endlatex = '&fg=' + style.textcolor

# At the beginning, the commands \$, \% and \& are temporarily
# replaced by placeholders (the second entry in each 4-tuple).
# At the end, The placeholders in text mode are replaced by
# the third entry, and the placeholders in math mode are
# replaced by the fourth entry.

esc = [['\\$', '_dollar_', '&#36;', '\\$'],
       ['\\%', '_percent_', '&#37;', '\\%'],
       ['\\&', '_amp_', '&amp;', '\\&'],
       ['>', '_greater_', '>', '&gt;'],
       ['<', '_lesser_', '<', '&lt;']]

standard_macros = [['\\more', '<!--more-->'],
                   ['\\newblock', '\\\\'],
                   ['\\sloppy', ''],
                   ['\\S', '&sect;']]

Mnomath = [['\\\\', '<br/>\n'],
           ['\\ ', ' '],
           ['\\`a', '&agrave;'],
           ['\\\'a', '&aacute;'],
           ['\\"a', '&auml;'],
           ['\\aa ', '&aring;'],
           ['{\\aa}', '&aring;'],
           ['\\`e', '&egrave;'],
           ['\\\'e', '&eacute;'],
           ['\\"e', '&euml;'],
           ['\\`i', '&igrave;'],
           ['\\\'i', '&iacute;'],
           ['\\"i', '&iuml;'],
           ['\\`o', '&ograve;'],
           ['\\\'o', '&oacute;'],
           ['\\"o', '&ouml;'],
           ['\\`o', '&ograve;'],
           ['\\\'o', '&oacute;'],
           ['\\"o', '&ouml;'],
           ['\\H o', '&ouml;'],
           ['\\`u', '&ugrave;'],
           ['\\\'u', '&uacute;'],
           ['\\"u', '&uuml;'],
           ['\\`u', '&ugrave;'],
           ['\\\'u', '&uacute;'],
           ['\\"u', '&uuml;'],
           ['\\v{C}', '&#268;']]

cb = re.compile(r'{|}')


def find_macros(s):
    keys = re.findall(r'\\def(.*?){', s)
    chunks = re.split(r'\\def.*?{', s)
    return [(key, to_closing_bracket(chunk)) for key, chunk in zip(keys, chunks[1:])]


def to_closing_bracket(chunk):
    height = 1
    idx = -1
    try:
        while height > 0:
            idx += 1
            if chunk[idx] == '\\':
                idx += 1
                letters = re.match(r'[a-zA-Z]*', chunk[idx:]).group(0)
                idx += max(len(letters) - 1, 0)
            elif chunk[idx] == '{':
                height += 1
            elif chunk[idx] == '}':
                height -= 1
        return chunk[:idx]
    except IndexError:
        raise ParseError('group has no closing bracket')


def extractbody(m):
    r"""
    Extract the text in \begin{document}...\end{document}, if present; otherwise keep everything. Also remove
    comments, normalize spacing, process ifs and replace $$ by \[ and \].
    """
    # look for \begin{document}...\end{document}
    match = re.search(r'\\begin{document}.*\\end{document}', m, re.DOTALL)
    if not match:
        raise ParseError('no \\begin{document}...\\end{document} found')
    m = match.group(0)

    # replace escaped characters by placeholders
    for e in esc:
        m = m.replace(e[0], e[1])

    m = re.sub(r'%.*', '', m)  # remove comments
    m = re.sub(r'\n\n+', '<p>', m)  # replace double newlines with <p>
    m = re.sub(r'\s+', ' ', m)  # replace other newlines and multiple spaces with a single space

    # process \if[false|tex|blog]...\fi sequences (assume no nesting)
    m = re.sub(r'\\iffalse.*?\\fi', '', m)
    m = re.sub(r'\\iftex.*?\\fi', '', m)
    m = re.sub(r'\\ifblog', '', m)
    m = re.sub(r'\\fi', '', m)

    # change $$...$$ to \[...\]
    split = re.split(r'\$\$', m)
    if len(split) % 2 == 0:
        raise ParseError('ended in math mode')
    m = split[0]
    for i in range(1, len(split), 2):
        m = m + '\\[' + split[i] + '\\]' + split[i + 1]

    # change eqnarray* environments to regular array environments
    m = m.replace('\\begin{eqnarray*}', '\\[ \\begin{array}{rcl} ')
    m = m.replace('\\end{eqnarray*}', '\\end{array} \\]')
    # todo: what about align*?

    return m


def subinputs(s):
    r = re.compile(r'\\input{.*?}')
    inputs = r.findall(s)
    rest = r.split(s)
    s = rest[0]
    for i in range(len(inputs)):
        filename = re.match(r'\\input{(.*?)}', inputs[i]).group(1)
        with open(filename, 'r') as tex_file:
            s += tex_file.read()
        s += rest[i+1]
    return s


def convertsqb(m):
    r = re.compile(r'\\item\s*\[.*?\]')

    Litems = r.findall(m)
    Lrest = r.split(m)

    m = Lrest[0]
    for i in range(0, len(Litems)):
        s = Litems[i]
        s = s.replace('\\item', '\\nitem')
        s = s.replace('[', '{')
        s = s.replace(']', '}')
        m = m + s + Lrest[i + 1]

    r = re.compile(r'\\begin\s*\{\w+}\s*\[.*?\]')
    Lthms = r.findall(m)
    Lrest = r.split(m)

    m = Lrest[0]
    for i in range(0, len(Lthms)):
        s = Lthms[i]
        s = s.replace('\\begin', '\\nbegin')
        s = s.replace('[', '{')
        s = s.replace(']', '}')
        m = m + s + Lrest[i + 1]

    return m


def converttables(m):
    retable = re.compile(r'\\begin{b?tabular}.*?\\end{b?tabular}')
    tables = retable.findall(m)
    rest = retable.split(m)

    m = rest[0]
    for i in range(len(tables)):
        m += convertonetable(tables[i])
        m += rest[i + 1]

    return m


def convertonetable(m):
    border = m.find('{btabular}') != -1
    tokens = re.compile(r'\\begin{b?tabular}{.*?}'
                        r'|\\end{b?tabular}'
                        r'|&|\\\\')

    align = {'c': 'center', 'l': 'left', 'r': 'right'}

    T = tokens.findall(m)
    C = tokens.split(m)

    L = cb.split(T[0])
    format = L[3]

    columns = len(format)
    if border:
        m = '<table border="1" align=center>'
    else:
        m = '<table align = center><tr>'
    p = 1
    i = 0

    while T[p - 1] != '\\end{tabular}' and T[p - 1] != '\\end{btabular}':
        m = m + '<td align=' + align[format[i]] + '>' + C[p] + '</td>'
        p = p + 1
        i = i + 1
        if T[p - 1] == '\\\\':
            for i in range(p, columns):
                m = m + '<td></td>'
            m = m + '</tr><tr>'
            i = 0
    m = m + '</tr></table>'
    return m


def convertmacros(m, extra_macros):
    comm = re.compile(r'\\[a-zA-Z]*')
    commands = comm.findall(m)
    rest = comm.split(m)

    r = rest[0]
    for i in range(len(commands)):
        for s1, s2 in standard_macros + extra_macros:
            if s1 == commands[i]:
                commands[i] = s2
        r = r + commands[i] + rest[i + 1]
    return r


def separatemath(m):
    mathre = re.compile(r'\$.*?\$'
                        r'|\\begin{equation}.*?\\end{equation}'
                        r'|\\\[.*?\\\]')
    math = mathre.findall(m)
    text = mathre.split(m)
    return math, text


def processmath(M, ref, count, html):
    R = []

    mathdelim = re.compile(r'\$'
                           r'|\\begin{equation}'
                           r'|\\end{equation}'
                           r'|\\\[|\\\]')
    label = re.compile(r'\\label{.*?}')

    for m in M:
        md = mathdelim.findall(m)
        mb = mathdelim.split(m)

        # In what follows, md[0] contains the initial delimiter,
        # which is either \begin{equation}, or $, or \[, and
        # mb[1] contains the actual mathematical equation

        if md[0] == '$':
            if html:
                m = m.replace('$', '')
                m = m.replace('+', '%2B')
                m = m.replace(' ', '+')
                m = m.replace('\'', '&#39;')
                m = '<img src="http://l.wordpress.com/latex.php?latex=%7B' + m + '%7D' + endlatex + '">'
            else:
                m = '$latex {' + mb[1] + '}' + endlatex + '$'

        else:
            if md[0].find('\\begin') != -1:
                count['equation'] += 1
                mb[1] = mb[1] + '\\ \\ \\ \\ \\ (' + str(count['equation']) + ')'
            if html:
                mb[1] = mb[1].replace('+', '%2B')
                mb[1] = mb[1].replace('&', '%26')
                mb[1] = mb[1].replace(' ', '+')
                mb[1] = mb[1].replace('\'', '&#39;')
                m = '<p align=center><img src="http://l.wordpress.com/latex.php?latex=\\displaystyle ' + mb[
                    1] + endlatex + '"></p>\n'
            else:
                m = '<p align=center>$latex \\displaystyle ' + mb[1] + endlatex + '$</p>\n'
            if m.find('\\label') != -1:
                mnolab = label.split(m)
                mlab = label.findall(m)

                # Now the mathematical equation, which has already
                # been formatted for WordPress, is the union of
                # the strings mnolab[0] and mnolab[1]. The content
                # of the \label{...} command is in mlab[0]
                lab = mlab[0]
                lab = cb.split(lab)[1]
                lab = lab.replace(':', '')
                ref[lab] = count['equation']

                m = '<a name="' + lab + '">' + mnolab[0] + mnolab[1] + '</a>'

        R = R + [m]
    return R


def convertcolors(m, c):
    if m.find('begin') != -1:
        return '<span style="color:#' + style.colors[c] + ';">'
    else:
        return '</span>'


def convertitm(m):
    if m.find('begin') != -1:
        return '\n\n<ul>'
    else:
        return '\n</ul>\n\n'


def convertenum(m):
    if m.find('begin') != -1:
        return '\n\n<ol>'
    else:
        return '\n</ol>\n\n'


def convertbeginnamedthm(thname, thm, count):
    count[style.theorems[thm]] += 1
    t = style.beginnamedthm.replace('_ThmType_', thm.capitalize())
    t = t.replace('_ThmNumb_', str(count[style.theorems[thm]]))
    t = t.replace('_ThmName_', thname)
    return t


def convertbeginthm(thm, count):
    count[style.theorems[thm]] += 1
    t = style.beginthm.replace('_ThmType_', thm.capitalize())
    t = t.replace('_ThmNumb_', str(count[style.theorems[thm]]))
    return t


def convertlab(m, ref, inthm, count):
    m = cb.split(m)[1]
    m = m.replace(':', '')
    if inthm != '':
        ref[m] = count[style.theorems[inthm]]
    else:
        ref[m] = count['section']
    return '<a name="' + m + '"></a>'


def convertproof(m, html):
    if m.find('begin') != -1:
        return style.beginproof
    else:
        return style.endproof(html)


def convertsection(m, count):
    L = cb.split(m)

    # L[0] contains the \\section or \\section* command, and
    # L[1] contains the section name

    if L[0].find('*') == -1:
        t = style.section
        count['section'] += 1
        count['subsection'] = 0

    else:
        t = style.sectionstar

    t = t.replace('_SecNumb_', str(count['section']))
    t = t.replace('_SecName_', L[1])
    return t


def convertsubsection(m, count):
    L = cb.split(m)

    if L[0].find('*') == -1:
        t = style.subsection
    else:
        t = style.subsectionstar

    count['subsection'] += 1
    t = t.replace('_SecNumb_', str(count['section']))
    t = t.replace('_SubSecNumb_', str(count['subsection']))
    t = t.replace('_SecName_', L[1])
    return t


def converturl(m):
    L = cb.split(m)
    return '<a href="' + L[1] + '">' + L[3] + '</a>'


def converturlnosnap(m):
    L = cb.split(m)
    return '<a class="snap_noshots" href="' + L[1] + '">' + L[3] + '</a>'


def convertimage(m):
    L = cb.split(m)
    return ('<p align=center><img ' + L[1] + ' src="' + L[3]
            + '"></p>')


def convertstrike(m):
    L = cb.split(m)
    return '<s>' + L[1] + '</s>'


def processtext(t, ref, count, html):
    p = re.compile('\\\\begin\\{\\w+}'
                   '|\\\\nbegin\\{\\w+}\\s*\\{.*?}'
                   '|\\\\end\\{\\w+}'
                   '|\\\\item'
                   '|\\\\nitem\\s*\\{.*?}'
                   '|\\\\label\\s*\\{.*?}'
                   '|\\\\section\\s*\\{.*?}'
                   '|\\\\section\\*\\s*\\{.*?}'
                   '|\\\\subsection\\s*\\{.*?}'
                   '|\\\\subsection\\*\\s*\\{.*?}'
                   '|\\\\href\\s*\\{.*?}\\s*\\{.*?}'
                   '|\\\\hrefnosnap\\s*\\{.*?}\\s*\\{.*?}'
                   '|\\\\image\\s*\\{.*?}\\s*\\{.*?}\\s*\\{.*?}'
                   '|\\\\sout\\s*\\{.*?}')

    for s1, s2 in Mnomath:
        t = t.replace(s1, s2)

    ttext = p.split(t)
    tcontrol = p.findall(t)

    w = ttext[0]

    i = 0
    inthm = ''
    while i < len(tcontrol):
        if tcontrol[i].find('{itemize}') != -1:
            w = w + convertitm(tcontrol[i])
        elif tcontrol[i].find('{enumerate}') != -1:
            w = w + convertenum(tcontrol[i])
        elif tcontrol[i][0:5] == '\\item':
            w = w + '<li>'
        elif tcontrol[i][0:6] == '\\nitem':
            lb = tcontrol[i][7:].replace('{', '')
            lb = lb.replace('}', '')
            w = w + '<li>' + lb
        elif tcontrol[i].find('\\hrefnosnap') != -1:
            w = w + converturlnosnap(tcontrol[i])
        elif tcontrol[i].find('\\href') != -1:
            w = w + converturl(tcontrol[i])
        elif tcontrol[i].find('{proof}') != -1:
            w = w + convertproof(tcontrol[i], html)
        elif tcontrol[i].find('\\subsection') != -1:
            w = w + convertsubsection(tcontrol[i], count)
        elif tcontrol[i].find('\\section') != -1:
            w = w + convertsection(tcontrol[i], count)
        elif tcontrol[i].find('\\label') != -1:
            w = w + convertlab(tcontrol[i], ref, inthm, count)
        elif tcontrol[i].find('\\image') != -1:
            w = w + convertimage(tcontrol[i])
        elif tcontrol[i].find('\\sout') != -1:
            w = w + convertstrike(tcontrol[i])
        elif tcontrol[i].find('\\begin') != -1 and tcontrol[i].find('{center}') != -1:
            w = w + '<p align=center>'
        elif tcontrol[i].find('\\end') != -1 and tcontrol[i].find('{center}') != -1:
            w = w + '</p>'
        else:
            for clr in style.colors:
                if tcontrol[i].find('{' + clr + '}') != -1:
                    w = w + convertcolors(tcontrol[i], clr)
            for thm in style.theorems:
                if tcontrol[i] == '\\end{' + thm + '}':
                    w = w + style.endthm
                    inthm = ''
                elif tcontrol[i] == '\\begin{' + thm + '}':
                    w = w + convertbeginthm(thm, count)
                    inthm = thm
                elif tcontrol[i].find('\\nbegin{' + thm + '}') != -1:
                    L = cb.split(tcontrol[i])
                    thname = L[3]
                    w += convertbeginnamedthm(thname, thm, count)
                    inthm = thm
        w += ttext[i + 1]
        i += 1

    return processfontstyle(w)


def processfontstyle(w):
    close = dict()
    ww = ''
    level = i = 0
    while i < len(w):
        special = False
        for k, v in style.fontstyle.items():
            l = len(k)
            if w[i:i + l] == k:
                level += 1
                ww += '<' + v + '>'
                close[level] = '</' + v + '>'
                i += l
                special = True
        if not special:
            if w[i] == '{':
                ww += '{'
                level += 1
                close[level] = '}'
            elif w[i] == '}' and level > 0:
                ww += close[level]
                level -= 1
            else:
                ww += w[i]
            i += 1
    return ww


def convertref(m, ref):
    p = re.compile(r'\\ref\s*\{.*?}|\\eqref\s*\{.*?}')

    T = p.split(m)
    M = p.findall(m)

    w = T[0]
    for i in range(len(M)):
        t = M[i]
        lab = cb.split(t)[1]
        lab = lab.replace(':', '')
        if t.find('\\eqref') != -1:
            w = w + '<a href="#' + lab + '">(' + str(ref[lab]) + ')</a>'
        else:
            w = w + '<a href="#' + lab + '">' + str(ref[lab]) + '</a>'
        w = w + T[i + 1]
    return w


def convert_one(s, html=False):
    r"""
    Convert one latex string to HTML.

    The program makes several passes through the input.

    In a first clean-up, all text before \begin{document}
    and after \end{document}, if present, is removed,
    all double-returns are converted
    to <p>, and all remaining returns are converted to
    spaces.

    The second step implements a few simple macros. The user can
    add support for more macros if desired by editing the
    convertmacros() procedure.

    Then the program separates the mathematical
    from the text parts. (It assumes that the document does
    not start with a mathematical expression.)

    It makes one pass through the text part, translating
    environments such as theorem, lemma, proof, enumerate, itemize,
    \em, and \bf. Along the way, it keeps counters for the current
    section and subsection and for the current numbered theorem-like
    environment, as well as a  flag that tells whether one is
    inside a theorem-like environment or not. Every time a \label{xx}
    command is encountered, we give ref[xx] the value of the section
    in which the command appears, or the number of the theorem-like
    environment in which it appears (if applicable). Each appearence
    of \label is replace by an html "name" tag, so that later we can
    replace \ref commands by clickable html links.

    The next step is to make a pass through the mathematical environments.
    Displayed equations are numbered and centered, and when a \label{xx}
    command is encountered we give ref[xx] the number of the current
    equation.

    A final pass replaces \ref{xx} commands by the number in ref[xx],
    and a clickable link to the referenced location.
    """
    ref = {}

    # prepare variables computed from the info in latex2wpstyle
    count = {counter: 0 for counter in style.theorems.values()}
    count['section'] = count['subsection'] = count['equation'] = 0

    # process all def-macros
    macros = find_macros(s)

    # extracts text between \begin{document} and \end{document}, normalizes spacing
    s = extractbody(s)

    # process latex \input{...}
    s = subinputs(s)

    # formats tables
    s = converttables(s)

    # reformats optional parameters passed in square brackets
    s = convertsqb(s)

    # implement simple macros
    s = convertmacros(s, macros)

    # extracts the math parts, and replaces the with placeholders
    # processes math and text separately, then puts the processed
    # math equations in place of the placeholders
    (math, text) = separatemath(s)

    s = text[0]
    for i in range(len(math)):
        s = s + '__math' + str(i) + '__' + text[i + 1]

    s = processtext(s, ref, count, html)
    math = processmath(math, ref, count, html)

    # converts escape sequences such as \$ to HTML codes
    # This must be done after formatting the tables or the '&' in
    # the HTML codes will create problems
    for e in esc:
        s = s.replace(e[1], e[2])
        for i in range(len(math)):
            math[i] = math[i].replace(e[1], e[3])

    # puts the math equations back into the text
    for i in range(len(math)):
        s = s.replace('__math' + str(i) + '__', math[i])

    # translating the \ref{} commands
    s = convertref(s, ref)

    if html:
        s = '<head><style>body{max-width:55em;}a:link{color:#4444aa;}a:visited{color:#4444aa;}a:hover{' \
            'background-color:#aaaaFF;}</style></head><body>' + s + '</body></html>'

    s = s.replace('<p>', '\n<p>\n')

    return s


def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Convert LaTeX file to WordPress-ready HTML')
    parser.add_argument('input_file', nargs='+', help='files to convert')
    parser.add_argument('--html', action='store_true', help='produce standard HTML instead of WordPress stuff')
    args = parser.parse_args()

    for input_file in args.input_file:
        output_file = os.path.splitext(os.path.basename(input_file))[0] + '.html'
        with open(input_file, 'r') as input_stream:
            latex = input_stream.read()
        html = convert_one(latex, args.html)
        with open(output_file, 'w') as output_stream:
            output_stream.write(html)
