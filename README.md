### How to install

You need python 3.6+. You can install latex2wp using pip:

`pip install git+https://github.com/seaneberhard/latex2wp`.

### How to use

Use template/post-template.tex as a starting point, writing your text between the `\begin{document}` and `\end{document}`. In the directory of your tex file, do

`latex2wp yourlatexfile.tex`.

This will produce a file called `yourlatexfile.html`, which is ready to be cut and pasted into WordPress. Pure HTML can be produced by adding the `--html` option.

For more information, try

`latex2wp --help`.

--------------------

### What works and what doesn't

See the file `latex2wp/test/resources/example.tex` to see how to import figures, have text appear in different colors, have links to URLs, and enter the "more" command of WordPress.

Anything between `\iftex...\fi` is compiled in LaTeX but ignored in the conversion to WordPress; anything between `\ifblog...\fi` is converted to WordPress but ignored by LaTeX. Anything between `\iffalse...\fi` is ignored by both.

There is very limited support for macros. All macros must be defined with `\def`, they must have no arguments, they must be independent, and they must appear outside the main `\begin{document}...\end{document}` block.

Several theorem-like numbered environments are supported,
such as `theorem`, `lemma`, `proposition`, `conjecture`, `remark`, `corollary`, `example`, and `exercise`. In addition, there is the `proof` environment.

You can use the inline math environment `$...$` and the displayed math environments `$$...$$`, `\[...\]`, `\begin{equation}...\end{equation}`. WordPress has some limitations to the kind of latex equations it can display. As a consequence, `align` and `eqnarray` are not supported. You can, however, use `eqnarray*`, and you can use `array` inside a math environment.

The tabular environment works.

The reference commands `\label{}`, `\eqref{}`, and `\ref{}` work in the standard way.

There is no support for `\medskip`, `\bigskip` and other such formatting commands. The return command `\\` is recognized.

`\section`, `\section*`, `\subsection` and `\subsection*` are supported, but not `\subsubsection` and so on. 

There is no support for bibliographic references or footnotes.

------------------------

### How to customize

The file `latex2wp/style.py` can be easily modified to add to add new theorem-like environments or change their numbering conventions, or to change the typesetting design of theorem-like environments and other details. To do this you will need to clone the git repo, and pip install your local version by doing `pip install .` in your checkout.

For example, suppose you want to change the formatting of theorem-like environments. The string `beginthm` specifies what to do at the beginning of a theorem-like environment. In the string, `_ThmType_` will be replaced by the type of theorem (e.g. `Theorem`, or `Lemma`, or `Corollary`, etc.) and `_ThmNumb_` will be replaced by the theorem number. So the standard setting

`beginthm= "\n<blockquote><b>_ThmType_ _ThmNumb_</b> <em>"`

will start a blockquote environment, write in boldface something like "Theorem 3", and then start an emphasized environment. `beginnamedthm` specifies what to do at the beginning of a theorem-like environment declared by something like

`\begin{theorem}[Fundamental Theorem of Calculus]...`

the string `_ThmName_` holds the content of the text in square brackets in the original LaTeX. `endthm` specifies what to do at the end of a theorem-like environment.

### Please contribute!

If you do make changes that you think would be useful to other people, please contribute! Github makes contributing easy. If you need any help just get in touch.

---

### Changelog

Version 1.0, 2018-09-30
  - Migrate project to github
  - Migrate to Python 3
  - Enable installation by pip
  - Package up and add commandline entrypoint `latex2wp`

Version 0.6.2, 2009-05-06
  - Additional support for accented characters
  - Convert '>' and '<' to HTML codes
  - Changed to handling of \& and \% in math mode to reflect
    different WordPress treatment of them

Version 0.6.1, 2009-02-23
  - Simplified format of latex2wpstyle.py (by Radu Grigore)
  - Allow nesting of font styles such as \bf and \em (by Radu Grigore)
  - Allow escaped symbols such as \$ in math mode
  - LaTeX macros are correctly "tokenized"
  - Support eqnarray* environment


Version 0.6, 2009-02-21 -  First release
