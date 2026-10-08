---
name: bias
aliases: [xbias]
also_documents: []
source: XSbias.tex
---

# bias

**predict the bias of the current fit under the W statistic**

**Syntax:** `bias` [`draws` <n>]

When a spectrum is fitted with `statistic` `cstat` and a
Poisson background spectrum has been read in, XSPEC minimises the W
statistic (Appendix AppendixStatistics), which profiles out one
nuisance background rate per source bin.  For a sparse background those
per-bin estimates are noisy and, because their number grows with the data,
they bias the fitted source parameters --- for a faint source on a
low-count background by tens of percent.  `bias` predicts that bias
for the fit at hand: it solves the expected estimating equation
$E[U(\theta)]=0$ for the hypothesized truth $\theta_0$ whose expected
estimate is the fitted value $\hat\theta$, with the loaded background
pooled to about 25 counts per super-bin as its estimate of the true
background rate.  It is a diagnostic: nothing is corrected, and on return
every parameter holds its fitted value.

The output is one line per free parameter (columns abbreviated here to fit
the page):

```
  par component parameter unit      fitted  fit sigma  first-order  debiased      bias  bias %
    1 phabs     nH        10^22    0.94894    0.04981   -0.0009436   0.94993  -0.00099  -0.104
    2 powerlaw  PhoIndex           2.39963    0.05837    -0.001689   2.40138  -0.00175  -0.073
    3 powerlaw  norm               0.74311    0.05633    -0.001332   0.74450  -0.00139  -0.186
```

where `fitted` is the fitted value, `fit sigma` its
1-$\sigma$ uncertainty from the fit covariance (so that the bias can be
read against the statistical error), `debiased` is $\theta_0$,
`bias` is $\hat\theta-\theta_0$ in parameter units and
`bias %` is $100\,(\hat\theta-\theta_0)/\theta_0$.  The
`first-order` column is the linear-regime estimate of the bias at
the fitted values; it and the full solve agree when the bias is small
compared with the parameter's scale, and they separate as the bias grows.
The lines above the table say how many super-bins the background rate was
estimated from and what fraction of the source bins sit at the background
floor (the profiled rate at its lower bound), which is the sparse-background
regime that produces the bias.

The prediction is an expectation over both the source and the background
realizations.  A parameter that is set by a few channels --- a line
centroid or width --- can realize a bias on any one dataset well away from
the expected value; the numbers are most trustworthy for continuum
parameters.

**Collapse.** When the fit has left the regime where the
estimator tracks the truth --- the estimator's expected value no longer
moves with the true parameters, so no hypothesized truth reproduces the
fitted values --- no bias number is meaningful.  `bias` then prints a
verdict in place of the table, saying that the fit is in that regime and
that the remedy is to pool the background with
`group` `back` and refit.  This is the same remedy as for a
large predicted bias: `group` `back` `auto` shrinks the
number of nuisance parameters and brings the bias down to a few percent
(see the `group` command), after which `bias` can be run again
on the pooled fit.

**Pooled backgrounds.** With an ungrouped background the
expected estimating equation is evaluated exactly, bin by bin, and the
result is deterministic.  With a pooled background
(`group` `back`) the pooled score has no closed form and is
averaged over Monte Carlo realizations of each super-bin,
`<n>` per super-bin (default 2000), drawn from XSPEC's random
generator: `xset` `seed` immediately before the command
reproduces the run.  A run on a pooled background typically takes a few
seconds; an ungrouped run well under a second.

`bias` requires a valid `fit` first, and is refused for any
spectrum whose statistic is not `cstat` with a Poisson background
(`chi`, `pgstat`, `lstat`, or `cstat` with no
background --- with no profiled background rate there is no W-statistic
bias to predict), for a free response (`gain`) parameter, and for a
model with no free parameter.  Several spectra in a joint fit are handled
together.  The results of the last `bias` can be retrieved with
`tclout` `bias`, and PyXspec has `Fit.bias()`.  The
method is described in Arnaud (2026), *Bias in the W statistic*, and
in Appendix AppendixStatistics.

**Examples:**

```
XSPEC> data src.pha
XSPEC> back bgd.pha
XSPEC> statistic cstat
XSPEC> model phabs(powerlaw)
XSPEC> fit
XSPEC> bias
// predicted bias per free parameter, beside the fit sigma
XSPEC> group back auto
XSPEC> fit
XSPEC> xset seed 4321
XSPEC> bias draws 4000
// the pooled fit, 4000 Monte Carlo draws per super-bin, reproducible
XSPEC> tclout bias percent
// the predicted bias in percent, one number per free parameter
```
