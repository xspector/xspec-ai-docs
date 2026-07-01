---
name: addline
aliases: []
also_documents: []
source: XSaddline.tex
---

# addline

**add spectral lines to a model**

Tcl script to add one or more lines to the current model in an optimum fashion. 

**Syntax:** `addline` [<nlines>] [<modeltype>] [fit| nofit]

`<nlines>` additional lines are added one at a time. Line energies 
are set to that of the largest residual between the data and the model. 
For each line a fit is performed with the line width and normalization as 
the only free parameters. The default option is one gaussian line. The 
other `<modeltype>` that can be used is lorentz. If no third argument is 
given then the sigma and normalization of each line are fit. If `nofit`
is specified then the fit is not performed but if `fit` is specified 
then all free parameters are fit. 

`addline` currently will only work with the default model (i.e. not 
for named models).
