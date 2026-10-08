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
distributions only), or read back with `tclout margin`.  This command 
does not require that spectral data files are loaded, or that a valid fit must 
exist.

Alongside the marginal distribution, `margin` also builds the 
*integrated* (cumulative) probability over the same grid, by accumulating 
the bins in order of decreasing probability density.  The value in a bin is 
therefore the posterior mass held by every bin at least as dense as that one --- 
the smallest highest-density region containing it --- so it is not monotonic in 
bin order: the modal bin carries the lowest value and empty bins sit at 1.  This 
is what `plot integprob` contours, and its values may be read back with 
`tclout margin integprob`.

**The integrated probability is normalized over the margin grid, not over 
the whole posterior.**  A grid that does not cover the bulk of the distribution 
still produces contours summing to 1, so a nominal 68% region is 68% of the 
mass *inside the grid*.  The `fraction` column is normalized by all 
chain points instead, so summing it (`tclout margin fraction`) shows what 
share of the posterior the grid actually captured; if that total is well below 
1, widen the grid before interpreting the contours.

**Examples:**

Assuming chain(s) are loaded consisting of 4 parameters.  

```
XSPEC>margin 1 10.0 12.0 20 log 3 1.0 10.0 5
// Calculate a 2-D probability distribution of parameter 1 from 
// 10.0-12.0 in 20 linear bins, and parameter 3 from 1.0-10.0 in 
// 5 logarithmic bins.
XSPEC>margin 2 10.0 100.0 10 nolog 4 20. 30. 10
// Now calculate for parameter 2 in 10 log bins and 
// parameter 4 in 10 linear bins.
```
