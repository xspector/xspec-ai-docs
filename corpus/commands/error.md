---
name: error
aliases: [derror, rerror, uncertain, xderror, xerror, xrerror, xuncertain]
also_documents: [rerror, derror, uncertain]
source: XSerror.tex
---

# error (and rerror, derror)

**determine confidence intervals of a fit**

Determine the confidence region for a model parameter.

**Syntax:** `error` [[stopat <ntrial> <toler>] [maximum 
<redchi>] [nonew] [<delta fit statistic>] [<model param range>...]]

where `<model param range>` ::= `[<modelName>:]<first param> -
<last param>`

determines the ranges of parameters to be examined, and `<delta fit statistic>`
 (distinguished from the model parameter indices by the inclusion of a decimal point), 
 is the change in fit statistic used. 

**For response parameters** (see the `rmodel` and `gain` commands), use `rerror`
with identical syntax except:

`<response param range>` ::= `[<sourceNum>:]<first param> - 
<last param>`

**For data parameters** (see the `dmodel` command), use `derror` with data parameter numbers.

The `error` command uses one of two algorithms.  If Monte Carlo Markov Chains 
are loaded (see `chain` command) the error range is determined by sorting 
the chain values, and then taking a central percentage of the values 
corresponding to the confidence level as indicated by `<delta fit statistic>`.  
This is likely to be the faster of the two algorithms.

When chains are **not** loaded, `error`'s algorithm is as follows:

Each indicated parameter is varied, within its allowed hard limits, until 
the value of the fit statistic, minimized by allowing all the other non-frozen 
parameters to vary, is equal to the last value of fit statistic determined by 
the `fit` command plus the indicated `<delta fit statistic>`, to 
within an absolute (not fractional) tolerance of `<toler>`. Note that 
before the `error` command is executed, the data must be fitted. The 
initial default values are the range 1-1 and the `<delta fit statistic>`
of 2.706, equivalent to the 90% confidence region for a single interesting 
parameter. The number of trials and the tolerance for determining when 
the critical fit statistic is reached can be modified by preceeding them 
with the `stopat` keyword. Initially, the values are 20 trials with 
a tolerance of 0.01 in fit statistic.

Each trial value of the parameter is a fit of the other parameters with the
parameter frozen.  By default (`xset` `ERROR_SEARCH newton`)
that fit starts from the other parameters extrapolated from the previous
trials, and the next trial value is a Newton step (until the target is
bracketed) or the root of a Hermite cubic through the bracket (after) on
$\sqrt{\Delta S}$, which is nearly linear in the parameter near a minimum;
the slope at each trial is the derivative of the statistic in that
parameter with the others held at their fitted values.  A trial whose
extrapolated start gives a statistic outside the bracket is refitted from
the best fit before the search reports non-monotonicity.  This typically
needs about 0.6 of the model calculations of the earlier search, and can
also find the profile where a fit started from the best fit sticks at a
boundary.  `xset` `ERROR_SEARCH classic` runs the earlier
search: every trial fitted from the best fit, the step doubled until the
target is bracketed, then a 3-point quadratic.  The bounds of the two agree
to within the tolerance.  At chatter 15 each trial says which kind of step
it took, and each bound ends with a line giving its trials, fit iterations
and model calculations (Appendix AppendixAlgorithmsErrorSearch).

Every search starts from the best fit refitted with all the parameters free,
and is measured from that statistic and parameter value; the first one
refits before it starts, and each search ends with the same refit, so the
later ones start there too.  The result for a parameter therefore does not
depend on which other parameters are in the same `error` command or in
what order, and is the same with `parallel error`.  If that refit
improves on the fit by more than the fit's critical delta, it counts as a
new minimum.

If a new minimum is found in the course of finding the error, the default
behavior is to abort the calculation and then automatically rerun it using
the new best fit parameters.  If autosaving is enabled (see
`autosave`), the new best fit is written to the autosave file before
the calculation restarts, so it is recoverable even if the rerun is
interrupted. If you prefer not to automatically rerun the 
`error` calculation, then enter `nonew` at the start of the 
command string. The rerun only happens if the new fit is genuinely better: 
if re-fitting with all parameters free does not lower the fit statistic by 
more than the critical delta of the `method` command, `error` 
reports that and stops instead of restarting. If you see this warning, try
refitting with a smaller critical delta. 
The maximum keyword ensures that `error` will not be 
run if the reduced chi-squared of the best fit exceeds `<redchi>`. 
The default value for `<redchi>` is 2.0.

Since there are very many scenarios which may cause an `error` 
calculation to fail, it is highly recommended that you check the results 
by viewing the 9-letter error string, which is part of the output from the 
`tclout error` command (see `tclout` for a description of the 
error string).  If everything went well, the error string should be ``FFFFFFFFF''.

**Examples:**

```
//Assume that the current model has four model parameters.

XSPEC> error 1-4
//Estimate the 90% confidence ranges for each parameter.
XSPEC> error 9.0
//Estimate the confidence range for parameters 1-4 with delta fit
// statistic = 9.0, equivalent to the 3 sigma range.
XSPEC> error 2.706 1 3 1. 2
//Estimate the 90% ranges for parameters 1 and 3, and the 1. sigma 
// range for parameter 2.
XSPEC> error 4
//Estimate the 1. sigma range for parameter 4.
XSPEC> error nonew 4
//Same as before, but calculation will NOT automatically restart
//if a new minimum is found.
XSPEC> error stop 20,,3
//Estimate the 1-sigma range for parameter 3 after resetting the 
//number of trials to 20.Note that the tolerance field had to be 
//included (or at least skipped over).
 
```
