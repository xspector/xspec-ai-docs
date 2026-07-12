---
class: FitManager
singleton: Fit
module: fit.py
---

# Fit

Singleton instance `Fit` (class `FitManager`).

**Xspec fitting class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| bayes | str | get/set | Turn Bayesian inference on or off [string]. |
| bayesPriors | str | get | The current Bayesian prior settings, as a listing [string] |
| covariance | — | get | The covariance matrix from the most recent fit [tuple |
| criticalDelta | float | get/set | Critical delta for fit statistic convergence [float]. |
| delta | float | get/set | Set fit delta values to be proportional to the parameter value [float]. |
| dof | int | get | The degrees of freedom for the fit [int] (GET only). |
| method | str | get/set | The fitting algorithm to use [string]. |
| nIterations | int | get/set | The maximum number of fit iterations prior to query [int]. |
| nullhyp | — | get | The null hypothesis probability for the chi-sq fit (GET only). |
| nVarPars | int | get | The number of variable parameters for the fit [int] (GET only). |
| previousGoodness | float | get | The goodness value from the immediately previous call [float] (GET only). |
| previousGoodnessSims | list | get | The array of simulation values from the immediately previous goodness calculation [list] (GET only). |
| query | str | get/set | The fit query setting [string]. |
| useChainRule | str | get/set | The fit useChainRule setting [string]. |
| statistic | float | get | Fit statistic value from the most recent fit [float] (GET only). |
| statMethod | str | get/set | The type of fit statistic in use [string]. |
| statTest | str | get/set | The type of test statistic in use [string]. |
| testStatistic | float | get | Test statistic value from the most recent fit [float] (GET only). |
| globalBasins | — | get | Competitive basins from the most recent Fit.globalFit() or |
| weight | str | get/set | Change the weighting function used in the calculation of chi-sq [string]. |

## Methods

- `__init__()`
- `error(argString, respPar=False)` — Determine confidence intervals of a fit.
- `ftest(chisq2, dof2, chisq1, dof1)` — Calculate the F-statistic and its probability given new and old
- `goodness(nRealizations=100, sim=False, fit='fit')` — Perform a Monte Carlo calculation of the goodness-of-fit.
- `simulate(nRealizations, fSigma=1.0, nostat=False, fit=False, hook=None)` — Bulk posterior-predictive simulation (the `sim` command).
- `improve()` — Try to escape the current minimum (warm-restart global search).
- `globalFit(maxGen=None, popSize=None)` — Perform a global fit (cold-start Differential Evolution + polish).
- `compare(alternatives, method='lm', useGlobal=False)` — Compare alternative models against the current model (model selection).
- `perform()` — Perform a fit.
- `renorm(setting=None)` — Renormalize the model to minimize statistic with current parameters.
- `show()` — Show fit information.
- `steppar(argString)` — Perform a steppar run.
- `stepparResults(arg)` — Retrieve values from the most recent steppar run.
