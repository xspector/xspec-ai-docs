---
name: margin
aliases: [xmargin]
also_documents: []
source: XSmargin.tex
---

# margin

**MCMC probability distribution**

Use the currently loaded MCMC chains to 
calculate a multi-dimensional probability distribution.

**Syntax:** `margin` <step spec.> [<step spec.> ...]

where `<step spec.>` ::= `[log| nolog] 
[<model name>:]<fit param index> <low value> 
<high value> <no. steps>`.

The indicated fit parameter is stepped from `<low value>` to 
`<high value>` in `<no. steps>`+1 trials.  The stepping is either 
linear or log.  Initially, the stepping is linear but this can be changed by 
the optional string `log` before the fit parameter index.  `nolog` 
will force the stepping to be returned to the linear form.  The number of 
steps is set initially to ten. If the parameter number is zero then
the fit statistic values are used. The results of the most recently run margin
command may be examined with `plot margin` (for 1-D and 2-D 
distributions only).  This command does not require that spectral data 
files are loaded, or that a valid fit must exist.

**Examples:**

Assuming chain(s) are loaded consisting of 4 parameters.  

```
XSPEC12>margin 1 10.0 12.0 20 log 3 1.0 10.0 5
// Calculate a 2-D probability distribution of parameter 1 from 
// 10.0-12.0 in 20 linear bins, and parameter 3 from 1.0-10.0 in 
// 5 logarithmic bins.
XSPEC12>margin 2 10.0 100.0 10 nolog 4 20. 30. 10
// Now calculate for parameter 2 in 10 log bins and 
// parameter 4 in 10 linear bins.
```
