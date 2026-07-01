---
name: fit
aliases: [xfit]
also_documents: [fitglobal]
source: XSfit.tex
---

# fit

**fit data**

Find the best fit model parameters for the current data by minimizing the
current statistic.

**Syntax:** `fit` <fit method parameters>

The arguments to fit depend on the fitting method currently in use. 
See the `method` command for details (and for the usage of the 
USE_CHAIN_RULE option in the user's startup Xspec.init file). 
Output from the `fit` command also depends on the fitting method 
currently in use.

Using the Levenberg-Marquardt algorithm, the parameters accepted are the 
maximum `<number of iterations>` before the user is prompted, the 
`<critical delta>`, which is the (absolute, not fractional) change in 
the statistic between iterations less than which the fit is deemed to 
have converged, and `<critical beta>`.

The `<critical beta>` provides an optional second stopping criterion, 
and it refers to the | beta|/N value reported during a Levenberg-Marquardt 
fit.  This is the norm of the vector derivatives of the statistic with 
respect to the parameters divided by the number of parameters.  At the 
best fit this should be zero, and so provides another measure of how well 
the fit is converging.  `<critical beta>` is set to a negative value 
by default, which renders it inactive.

Including the string `delay` as an argument to fit turns on delayed 
gratification. It is turned off by `nodelay`. Delayed gratification 
modifies the way the damping parameter is set and has been shown in many 
cases to speed up convergence. The default is `nodelay`.

If `<number of iterations>`, `<critical delta>`, `<critical beta>`, 
`delay`, or `nodelay` is entered through the `fit` 
command, it also becomes the future default value for the currently loaded 
fit `method` (ie. Levenberg-Marquardt).

**Examples:**

```
XSPEC12> fit
// Fit with the default number of iterations and critical delta 
// chi-squared.
XSPEC12> fit 60
// Fit with 60 as the number of iterations.
XSPEC12> fit  50 1.e-3
// Fit with 1.e-3 as the critical delta.
XSPEC12> fit 50 1.e-3  20.
// Same fit, but will now use |beta|/N = 20.0 as another stopping
// criterion in addition to that of the critical delta. 
XSPEC12> fit delay
// Same fit, but will now use delayed gratification.
```

**Global optimization (the `global` keyword)**
**Syntax:** `fit` `global` [<maxgen> [<popsize>]]

A plain `fit` is a *local* optimizer: from the current
parameter values it descends to the nearest minimum of the statistic.
On a multi-modal or degenerate parameter space --- common when fitting
several physically distinct models to the same data, or a model with
near-degenerate components --- it can converge to a local minimum that
is far from the global best fit, with the result depending on the
starting point.

Including the keyword `global` (any three-or-more-character prefix
of `global`) prefixes the fit with a derivative-free *global*
search.  XSPEC runs a Differential Evolution sweep over the soft-limit box
of every thawed parameter, moves to the best point it finds, and then
polishes that point with the current `method` (Levenberg--Marquardt,
`migrad`, or `simplex`).  Because the search uses only
statistic evaluations and never derivatives, it works for the entire model
library, including local models that provide no analytic gradients.  The
final statistic, parameter errors, and covariance are produced by the
ordinary polish, so they are identical in form to those of a normal
`fit`.

The search box is the soft (``min''/``max'') limit range of each parameter,
which is always finite, so `fit` `global` never refuses to
start.  A positive parameter whose range spans more than four decades (a
column density or normalisation, say) is searched in $\log_{10}$ so the
wide scale does not swamp the others; a parameter with a soft minimum of
zero and a very wide range draws a non-fatal warning, since its scale
cannot be inferred.  The optional <maxgen> sets the number of
Differential Evolution generations (default 200) and <popsize> the
population size (default automatic, $\mathrm{clamp}(10D, 15, 200)$ for $D$
thawed parameters); these are the only tunable controls.

`fit` `global` is *never-regress*: if the global search
plus polish does not improve on the statistic of the current fit, the
original parameters are restored and a message is printed, so running it on
an already-good fit cannot make it worse.  The run is reproducible under
`xset seed`, and the Differential Evolution likelihood batch can be
spread over $N$ processes with `parallel global` <N>.

After the fit, any *other* distinct minima within $\Delta\mathrm{stat}
< 9$ (about $3\sigma$ for one degree of freedom) of the best fit are
reported as competitive basins, with their $\Delta\mathrm{stat}$ and
parameter values.  These flag genuine degeneracies that a single best-fit
number hides; the suggestion is to test them as distinct models with
`compare`.  The basin list is also available in PyXspec as
`Fit.globalBasins` after `Fit.globalFit()`.

**Example:**

```
XSPEC12> fit global
 ... Differential Evolution search, then a normal polish ...

 fit global: 1 additional competitive basin(s) within delta-stat < 9
 of the best fit (stat = 243.95):
    basin       dStat          stat   parameters(in fit order)
       2      3.1846        247.14   2.0014, 0.00039876, ...
  (test these as distinct models with `compare`.)
XSPEC12> fit global 300 40
// Run a longer global search: 300 generations, population 40.
```
