---
name: iplot
aliases: [xiplot]
also_documents: [iplotscript]
source: XSiplot.tex
---

# iplot

**make a plot, and leave XSPEC in interactive plotting mode**

Interactive plotting on the current plot device.

**Syntax:** `iplot` <plot type>

This command works like the `plot` command (see the `plot` command 
description), but allows the user to change the plot and to add text to 
the plot interactively using the PLT package. For more information see
Appendix AppendixPLT.

**In a script.**When `iplot` runs from a
script (`@file`, `xspec - file`) or from input that is not a
terminal, the lines that follow it are PLT commands, exactly as they would be
typed at the `PLT>` prompt, up to a line beginning `exit`,
`quit` or `q` (any case). The plot is drawn, those commands
run, PLT exits, and the script continues with the next line as an XSPEC
command; the terminal is never read. A script is thus the transcript of an
interactive session:

```
iplot data
label top My source
hardcopy src.ps/cps
exit
fit
```

Every line up to the terminator goes to PLT -- XSPEC does not try to spot its
own commands inside the block, since the two share words -- so a missing
`exit` sends the rest of the script to PLT. If the script ends first,
the plot is drawn and closed and a warning names the script, the
`iplot` line and the number of lines PLT was given. The block lines are
echoed and logged with PLT's `PLT>` prompt. At a terminal
`iplot` is unchanged; a session recorded with `script` records
an `exit` after each `iplot`, so it replays. Commands that should
apply to every plot belong in `setplot command` instead; those are
still applied first. In PyXspec, `Plot.iplot("data", commands=[...])`
does the same.
