---
name: lrt
aliases: []
also_documents: []
source: XSlrt.tex
---

# lrt

**likelihood ratio test between two models**

Tcl script to perform a likelihood ratio test between two models. 

**Syntax:** `lrt` <niter> <model0_name> <model1_name> 
[<filename>]

Runs `<niter>` simulations of datasets based on `<model0_name>`, 
calculates the likelihood ratio for `<model1_name>` relative to 
`<model0_name>` (calculated by the statistic for `<model0_name>` 
minus the statistic for `<model1_name>`), and outputs the fraction of 
iterations with the likelihood ratio smaller than that for the data. If the 
optional filename is given then the simulation results are written to the file. 
The first line of the file contains the results for the data, the other lines 
the simulations. Each line comprises the statistic values for `<model0_name>`, 
the statistic value for `<model1_name>`, and the difference.

Before running this procedure you must have created command files called 
`<model0_name>`.xcm and `<model1_name>`.xcm which define the 
two models. A good way to do this is to set up the model then use save 
model to make the command file.
