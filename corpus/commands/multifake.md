---
name: multifake
aliases: []
also_documents: []
source: XSmultifake.tex
---

# multifake

**perform multiple fakeit iterations and save to file**

Tcl script to perform many iterations of fakeit and save the results in a 
FITS file.

**Syntax:** `multifake` <time>  <niter>  <outfile>

This script runs `<niter>` iterations of fakeit with an exposure of 
`<time>` and writes the results to `<outfile>`. Before running this 
procedure you have read in one (and only one) dataset along with its response 
and optional background and arf files. You must also have defined the model.

The output file is a FITS binary table with the columns being the value fit 
for each parameter in each iteration. The final column is the statistic 
value for that iteration.

Note that if an error occurs during the fit of a faked spectrum then -999 
is written for all parameters and the statistic value for that iteration.
