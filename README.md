HOW TO GET STARTED

Have latex2wp.py,latex2wpstyle.py, macrosblog.tex and your tex file
in the same directory. Use post-template.tex as a starting
point, writing your text between the \begin{document}
and \end{document}.

HOW TO USE

In the directory in which latex2wp.py and your
tex file are both present, type
   python latex2wp.py yourlatexfile.tex

this will produce a file called yourlatexfile.html which
is ready to be cut and pasted into WordPress.

--------------------


WHAT WORKS

See the file example.tex to see how to import figures, have
text appear in different colors, have links to URLs, and
enter the "more" command of WordPress.

Anything between a "\iftex . . . \fi" is compiled in LaTeX
but ignored in the conversion to WordPress; anything between
"\ifblog . . . \fi" is converted to WordPress but ignored
by LaTeX. Anything between a "\iffalse . . . \fi" is ignored
by both.

A few macros are predefined, such as \E for \mathop{\mathbb E},
\P for \mathop{\mathbb P} and so on.

Several theorem-like numbered environments are supported,
such as "theorem", "lemma", "proposition", "remark", "corollary",
"example" and "exercise. In addition, there is the "proof"
environment.

You can use the inline math environment $...$ and the
displayed math environments $$...$$, \[ ... \],
\begin{equation} ... \end{equation}, and
\begin{eqnarray*} ... \end{eqnarray*}.

The tabular environment works

\label{}, \eqref{} and \ref{} work in the standard way.

-------------------


WHAT DOESN'T WORK

WordPress has some limitations to the kind of latex equations
it can display. As a consequence, align and eqnarray are
not supported. You can, however, use eqnarray* and you can use
array inside a math environment.

There is no support for \medskip, \bigskip and other such 
formatting commands. The return command \\ is recognized.

\section, \section*, \subsection and \subsection* are supported,
but not \subsubsection and so on. 

There is no support for bibliographic references

There is no support for footnotes.

------------------------

HOW TO CUSTOMIZE

The file latex2wpstyle.py can be easily modified to
make the program create pure HTML, to add new macros,
to add new theorem-like environments or change their
numbering conventions, or to change the typesetting
design of theorem-like environments and other details.

- Creating pure HTML: 

  If the variable HTML is set to True
  at the beginning of the program, then pure HTML code
  is generated, which can be previewed locally with a browser.

- Adding new macros:

  The variable M in latex2wpstyle.py contains
  a list of pair of strings. For every pair, every occurrence
  of the first string is replaced by an occurrence of the second
  string. Add your own macros as needed. Note that a backslash \
  must be written twice as \\, and a quote sign " must be written 
  as \", so that for example the accent command \" must be written
  as \\\". Any macro you define in M must of course also be defined
  in macrosblog.tex in order for the latex file to be compiled
  and previewed as pdf.

- Numbering conventions of numbered theorem-like environments:

  As in the TeX compiler, the program keeps several counters,
  for sections, subsections, equations, and theorem-like environments.
  Often, one wants certain environments to share the same counter, so
  that for example Lemma 2 is followed by Theorem 3 even if Theorem 3
  is the first theorem to appear.

  The variable T declared at the beginning of the program is a table
  that specifies which counter is used for which environment. Change
  the assignment to follow different numbering conventions. Any
  number strictly less than numberofcounters can be used to denote
  a counter in T. Increase the value of numberofcounters if you want
  to use a bigger range of counters in T.


- Creating new theorem-like environments:

  Just add the name of the new environment, for example "conjecture",
  to the list ThmEnvs of currently supported environments. Choose a
  counter number, for example 0, to use for it, and add the entry
      "conjecture" : 0
  to T. Now the program recognizes \begin{conjecture}...\end{conjecture}
  and will number conjectures using counter 0. Add a \newtheorem
  definition in macrosblog.tex in order to be able to compile a
  latex file that uses this new environment. 


- Formatting of Theorem-like environments:

  The string beginthm specifies what to do at the
  beginning of a theorem-like environment. In the string,
  _ThmType_ will be replaced by the type of theorem
  (e.g. Theorem, or Lemma, or Corollary, etc.) and
  _ThmNumb_ will be replaced by the theorem number. 
  So the standard setting
   beginthm= "\n<blockquote><b>_ThmType_ _ThmNumb_</b> <em>"
  will start a blockquote environment, write in boldface
  something like "Theorem 3", and then start an emphasized
  environment.

  beginnamedthm specifies what to do at the beginning of
  a theorem-like environment declared by something like
      \begin{theorem}[Fundamental Theorem of Calculus] ....
  the string _ThmName_ holds the content of the text in
  square brackets in the original LaTeX

  endthm specifies what to do at the end of a theorem-like
  environment.

- Formatting of the proof environment

  Set the beginproof and endproof variables

- Formatting of sections and subsections

 Set the section, sectionstar, subsection, and subsectionstar 
 variables

