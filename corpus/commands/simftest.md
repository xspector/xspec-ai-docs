---
name: simftest
aliases: []
also_documents: []
source: XSsimftest.tex
---

# simftest

**estimate the F-test probability for adding a component**

Tcl script to generate simulated datasets and use these to estimate 
the F-test probability for adding a model component. 

**Syntax:** `simftest` <model_comp> <niter> [<filename>]

This script runs `<niter>` sets of simulated datasets to estimate the F-test 
probability for adding the additional model component number `<model_comp>`.  
If `<filename>` is specified then passes this to lrt.tcl to 
save likelihood ratio simulation information. The first line of the file 
written contains the results for the data, the other lines for the 
simulations. Each line comprises the statistic value for the model without 
`<model_comp>`, that for the model with `<model_comp>`, and the 
difference.

Before running this script the model should be set up including the additional 
component to be tested. The script will create temporary files 
model_with_comp.xcm and model_without_comp.xcm.
