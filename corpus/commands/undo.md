---
name: undo
aliases: [xundo]
also_documents: []
source: XSundo.tex
---

# undo

**undo the previous command**

Undo the affects of the previously entered xspec command.

**Syntax:** `undo` 

New for xspec version 12, the `undo` command will restore the state of 
the xspec session prior to the most recently entered command.  The current 
implementation does not allow restoration to more than one command back, 
so calling `undo` repeatedly will have no effect.  Also, a `plot` 
command cannot be undone.
