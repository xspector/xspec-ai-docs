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
| jointPriors | list | get | The joint prior terms in force [list] (GET only). |
| covariance | — | get | The covariance matrix from the most recent fit [tuple |
| analyticGradient | str | get/set | The analytic-gradient mode [string]: "auto", |
| criticalDelta | float | get/set | Critical delta for fit statistic convergence [float]. |
| delta | float | get/set | Set fit delta values to be proportional to the parameter value [float]. |
| deltaEscalation | — | get/set | Whether a Levenberg-Marquardt fit retries a zero |
| errorSearch | str | get/set | How Fit.error() searches for a confidence bound [string]. |
| dof | int | get | The degrees of freedom for the fit [int] (GET only). |
| method | str | get/set | The fitting algorithm to use [string]. |
| nIterations | int | get/set | The maximum number of fit iterations prior to query [int]. |
| geodesic | bool | get/set | Geodesic acceleration for the 'leven' method [bool]. |
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
- `addJointPrior(prior)` — Register a joint (multi-parameter) prior [dict].
- `clearJointPriors(kind=None)` — Remove joint prior terms.
- `jacobian(mode=None)` — Predicted counts and their derivatives with respect to each free
- `gradient(mode=None)` — The derivative of the fit statistic with respect to each free
- `error(argString, respPar=False)` — Determine confidence intervals of a fit.
- `ftest(chisq2, dof2, chisq1, dof1)` — Calculate the F-statistic and its probability given new and old
- `goodness(nRealizations=100, sim=False, fit='fit')` — Perform a Monte Carlo calculation of the goodness-of-fit.
- `simulate(nRealizations, fSigma=1.0, nostat=False, fit=False, hook=None)` — Bulk posterior-predictive simulation (the `sim` command).
- `improve()` — Try to escape the current minimum (warm-restart global search).
- `globalFit(maxGen=None, popSize=None)` — Perform a global fit (cold-start Differential Evolution + polish).
- `posterior()` — Credible intervals from the loaded chain, on `error`'s convention.
- `nestVerdict()` — The last `nest` run's verdict (the block's [WARN]/[INFO] lines).
- `hmcVerdict()` — The last `hmc` run's verdict.
- `bias(draws=2000, seed=None)` — Predict the W-statistic bias of the current fit (the `bias` command).
- `coverage(niter, params=None, method='error', level=None, file=None, seed=None)` — How often error (or chain) intervals contain the truth (the
- `lrt(niter, null, alternative, file=None, seed=None)` — Likelihood-ratio test of two models, calibrated by simulation (the
- `simftest(component, niter, file=None, seed=None)` — Likelihood-ratio test of one model component, calibrated by
- `dataScan(setups, par=None, coord=None, method=None, file=None)` — Refit the current model to alternative data setups and report
- `cgof(f=None, draws=2000, seed=None)` — C-statistic goodness of fit with model systematics (the `cgof` command).
- `cgofDelta(deltaC, k, f, mu=None)` — Corrected significance of a nested model component with systematics.
- `compare(alternatives, method='lm', useGlobal=False)` — Compare alternative models against the current model (model selection).
- `comparePresets()` — The compare preset registry, against the current model.
- `loadComparePresets(path)` — Add a compare preset registry file for this session.
- `perform()` — Perform a fit.
- `renorm(setting=None)` — Renormalize the model to minimize statistic with current parameters.
- `show()` — Show fit information.
- `steppar(argString)` — Perform a steppar run.
- `stepparResults(arg)` — Retrieve values from the most recent steppar run.
