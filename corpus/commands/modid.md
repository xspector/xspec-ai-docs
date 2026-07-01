---
name: modid
aliases: []
also_documents: []
source: XSmodid.tex
---

# modid

**write out possible IDs for lines in the model**

Tcl script to write out possible IDs for gaussian or lorentzian lines in the current model. 

**Syntax:** `modid` [<delta> | conf]

This script runs the `identify` command for every gaussian or lorentzian 
line included in the current model. If a number is given as an argument then 
that is used as the delta energy for identify. If the string `conf` 
is given as the argument then the last calculated confidence regions are 
searched for possible line IDs. If no argument is given then `conf`
is assumed.
