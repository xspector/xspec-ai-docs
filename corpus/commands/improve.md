---
name: improve
aliases: [ximprove]
also_documents: []
source: XSimprove.tex
---

# improve

**search for a better fit near the current one**

**Syntax:** `improve` 

The `improve` command tries to escape a local minimum without
restarting the fit from scratch.  It is the warm-restart counterpart of
`fit` `global`: starting from the current best fit, it runs a
short derivative-free Differential Evolution pass seeded in a shell
*around* the current parameter values, then polishes the best point it
finds with the current `method`.  Use it when a `fit` has
converged but you suspect it has settled in a local rather than the global
minimum --- `improve` perturbs the parameters outward, re-optimizes,
and keeps the new result only if it is better.

`improve` requires a valid `fit` first (it warm-starts from the
current parameters).  Like `fit` `global` it is
*never-regress*: if the search does not beat the current statistic the
original parameters are restored, so it can only help.  It works with every
fit `method` (in earlier versions `improve` was available only
for the Minuit methods; it now uses the same Differential Evolution
machinery as `fit` `global` for all of them).  The run can be
interrupted with Ctrl-C, which leaves the pre-command fit in place.

The difference from `fit` `global` is the scope of the search.
`improve` explores a *local* shell about the current fit, so it
is cheaper and is meant for refining a fit or hopping a nearby barrier;
`fit` `global` searches the full soft-limit box of every
parameter from scratch and is the tool for a genuinely global, multi-modal
problem.  As with `fit` `global`, any additional competitive
minima within $\Delta\mathrm{stat} < 9$ of the best fit are reported and are
available in PyXspec as `Fit.globalBasins`.

**Example:**

```
XSPEC12> fit
// Levenberg-Marquardt converges to a local minimum.
XSPEC12> improve
// Differential Evolution shell about that fit, then a polish; if a
// deeper minimum is found the parameters move there, otherwise they
// are left unchanged.
```
