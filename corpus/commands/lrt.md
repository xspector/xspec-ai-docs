---
name: lrt
aliases: [xlrt]
also_documents: []
source: XSlrt.tex
---

# lrt

**likelihood-ratio test between two models, calibrated by simulation**

Test a null model against an alternative by the likelihood ratio, with the
distribution of the ratio found by simulation rather than assumed
(Protassov et al. 2002, ApJ 571, 545).

**Syntax:** `lrt` <niter> <null model> <alternative model> [<filename>]

Each model is given as a model expression in braces (`{powerlaw}`),
as a file saved by `save model` preceded by `@`
(`@null.xcm`), or as `current`, the model as it is now.  An
expression model starts from the current model's parameter values where a
component and parameter of the same name is unique in both.

Both models are fitted to the data and the observed difference of the fit
statistics, null minus alternative, is recorded.  `<niter>` datasets
are then simulated from the null model at its best fit (as
`goodness` simulates them), both models are refitted to each, and the
p-value is the fraction of simulations whose difference is at least the
observed one, reported with its binomial error.  The alternative is fitted
twice each time, from its own best fit to the data and from the null's
values carried onto it by name, and the better fit is kept; a simulation
in which the alternative still ends worse than the null is counted and
reported (a local minimum).  If `<filename>` is given, its first line
holds the data's two statistics and their difference and each further line
those of one simulation.

Unlike `ftest`, the result is valid when the null sits on a boundary
of the alternative (a line normalisation at zero) and for multiplicative
components.  For one component of the current model, `simftest`
builds the null itself.

The models, parameter values, error bounds, covariance matrix and data are
as they were afterwards.  Each simulation draws from its own random stream,
so `xset seed` reproduces a run and `parallel lrt`
`<n>` spreads the simulations over processes without changing the
result.  The result can be read with `tclout lrt`.

**Examples:**

```
XSPEC> model phabs(powerlaw + gaussian)
XSPEC> fit
XSPEC> lrt 1000 {phabs(powerlaw)} current lrt.txt
// p for the line, from 1000 simulations of the line-free model.
XSPEC> lrt 500 @thermal.xcm @nonthermal.xcm
// Two saved models.
```
