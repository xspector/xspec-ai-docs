---
name: error
aliases: [rerror, uncertain, xerror, xrerror, xuncertain]
also_documents: [rerror, uncertain]
source: XSerror.tex
---

# error (and rerror)

**determine confidence intervals of a fit**

Determine the confidence region for a model parameter.

**Syntax:** `error` [[stopat <ntrial> <toler>] [maximum 
<redchi>] [nonew] [<delta fit statistic>] [<model param range>...]]

where `<model param range>` ::= `[<modelName>:]<first param> -
<last param>`

determines the ranges of parameters to be examined, and `<delta fit statistic>`
 (distinguished from the model parameter indices by the inclusion of a decimal point), 
 is the change in fit statistic used. 

**For response parameters** (see `gain` command), use `rerror`
with identical syntax except:

`<response param range>` ::= `[<sourceNum>:]<first param> - 
<last param>`

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

If a new minimum is found in the course of finding the error, the default 
behavior is to abort the calculation and then automatically rerun it using 
the new best fit parameters. If you prefer not to automatically rerun the 
`error` calculation, then enter `nonew` at the start of the 
command string. The maximum keyword ensures that `error` will not be 
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

XSPEC12> error 1-4
//Estimate the 90% confidence ranges for each parameter.
XSPEC12> error 9.0
//Estimate the confidence range for parameters 1-4 with delta fit
// statistic = 9.0, equivalent to the 3 sigma range.
XSPEC12> error 2.706 1 3 1. 2
//Estimate the 90% ranges for parameters 1 and 3, and the 1. sigma 
// range for parameter 2.
XSPEC12> error 4
//Estimate the 1. sigma range for parameter 4.
XSPEC12> error nonew 4
//Same as before, but calculation will NOT automatically restart
//if a new minimum is found.
XSPEC12> error stop 20,,3
//Estimate the 1-sigma range for parameter 3 after resetting the 
//number of trials to 20.Note that the tolerance field had to be 
//included (or at least skipped over).
 
```
