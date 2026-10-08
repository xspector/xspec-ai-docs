---
name: goodness
aliases: [xgoodness]
also_documents: []
source: XSgoodness.tex
---

# goodness

**perform a goodness of fit Monte-Carlo simulation**

Perform a Monte Carlo calculation of the goodness-of-fit.

**Syntax:** `goodness` [<# of realizations>] [sim| nosim]
  [fit| nofit]

This command simulates `<# of realizations>` spectra based on
the model and writes out the percentage of these simulations with the
test statistic less than that for the data. If the observed spectrum
was produced by the model then this number should be around 50%. This
command only works if the sole source of variance in the data is
counting statistics. The `sim| nosim` switch determines
whether each simulation will use parameter values drawn from a
Gaussian distribution centered on the best fit with sigma from the
covariance matrix. The `sim` switch turns on this option,
`nosim` turns it off in which case all simulations are drawn
from the best-fit model. The default starting setting is
`sim`. The `fit| nofit` switch determines whether
fitting will be performed on each simulated dataset to find the best
fit before calculation of the test statistic. The `fit` switch
turns on this option, `nofit` turns it off in which case the
test statistic is calculated immediately after creating the simulated
dataset. The default starting setting is `fit`. The goodness
calculation may be sped up by setting the `parallel` command's
`goodness` option to run multiple processes.  Each realization has
its own random-number stream, derived from the `xset` `seed`,
so the results are the same for any number of processes.

When the data form a covariance group fit with `statistic`
`chistokes` or `chicov`, each simulated dataset is drawn
jointly from the per-bin cross-spectrum covariance, so the Monte Carlo
distribution of the test statistic is correct; see the correlated-spectra
discussion in the Statistics appendix.
