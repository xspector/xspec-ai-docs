---
name: method
aliases: [xmethod]
also_documents: []
source: XSmethod.tex
---

# method

**change the fitting method**

Set the minimization method.

**Syntax:** `method` <algorithm> [<# of trials/evaluations>
 [<method-specific options>]]

where `<algorithm>` is the method in use and the other arguments are 
control values for the minimization. Their meanings are explained under the 
individual methods. The `migrad` and `simplex` methods are taken 
from the CERN Minuit2 package, with documentation located at  
http://seal.web.cern.ch/seal/MathLibs/Minuit2/html/index.html. If either of
these are used, then the `error` command will use the Minuit2 minos 
method to find the confidence regions.

**leven**

**Syntax:** `method` leven [<# of eval>] [<crit delta>]
  [<crit beta>]] [delay | nodelay] [geodesic | nogeodesic]

The default XSPEC minimization method using the modified Levenberg-Marquardt 
algorithm based on the CURFIT routine from Bevington. `<# of eval>` is 
the number of trial vectors before the user is prompted to say whether 
they want to continue fitting.  `<crit delta>` is the convergence 
criterion, which is the (absolute, not fractional) difference in fit 
statistic between successive iterations, less than which the fit is 
determined to have converged.

`<crit beta>` refers to the | beta| /N value reported 
during a fit.  This is the norm of the vector of derivatives of the 
statistic with respect to the parameters divided by the number of parameters.  
At the best fit this should be zero, and so provides another measure of 
how well the fit is converging.  When this is set to a positive value, it 
will provide another fit stopping criterion in addition to that 
of the `<crit delta>` setting.

Including the string `delay` as an argument turns on delayed 
gratification. It is turned off by `nodelay`. Delayed gratification 
modifies the way the damping parameter is set and has been shown in many 
cases to speed up convergence. The default is `nodelay`.

Including `geodesic` turns on geodesic acceleration (Transtrum &
Sethna 2012), and `nogeodesic` turns it off; the default is
`nogeodesic`.  Each iteration's step $\delta\theta_1$ gets a
second-order correction $\delta\theta_2$ for the curvature of the model
along it, at the cost of one more model calculation per iteration, which
helps where the minimum lies at the end of a long curved valley
(Appendix AppendixAlgorithmsGeodesic).  It pays when the derivatives
are finite differences --- table models, convolutions, a model without an
analytic gradient, or `xset` `DISABLE_ANALYTIC_GRAD` `yes`
--- because then an iteration costs about twice as many model calculations
as there are free parameters and saving iterations matters.  With analytic
derivatives an iteration costs about two model calculations, and the extra
one usually costs more than it saves.  `delay` alone is often as good;
the two can be combined.  It is not used with `usechainrule no`, with
a free response parameter, or with a dependent parameter limit (the fit
takes plain steps and says so at chatter 10).  The fits made by
`error`, `steppar` and the simulation commands inherit it, and
`save` writes it.  At chatter 15 a fit ends with its number of
iterations and model calculations.

`<# of eval>`, `<crit delta>`, `<crit beta>`, `delay`, 
`nodelay`, `geodesic` and `nogeodesic` may also be set
through the `fit` command.

This method requires the first derivatives of the statistic with respect
to the parameters, and an estimate of the second derivatives.  When every
component of the active models has a registered analytic gradient, the
first derivatives are by default computed analytically in a single pass
(Appendix AppendixAlgorithms); set
`xset` `DISABLE_ANALYTIC_GRAD` `yes` to revert to
finite differences (for example to reproduce fit paths from earlier
versions).  Under the default
`xset` `ANALYTIC_GRAD` `auto`, components whose
analytic gradient costs more than finite differences (at present table
models) use finite differences for their parameters in leven fits.  The second derivatives are by default estimated using an
analytic expression which assumes that partial 2nd derivatives of the
model with respect to its parameters may be ignored.  This may be changed
with `xset` `usechainrule` `no` (or by setting the
USE_CHAIN_RULE flag to `false` in the user's startup
Xspec.init initialization file); XSPEC will then differentiate
the statistic numerically, which can be noticeably slower.

A parameter whose curvature-matrix diagonal is zero is *pegged*: held
fixed for an iteration with the message that the fit is insensitive to it.
When its derivative is a finite difference, the zero is usually an artefact
of a step too small for the model to change (a narrow line moving within one
energy bin, a model that is piecewise constant on the energy grid), so leven
first retries the step $\times 10$, up to three times and never beyond 1%
of the parameter's hard range, keeping the larger step for the rest of that
fit.  Because a step that large is a coarse derivative, a fit in which a step
was raised is worth repeating: the next `fit` starts from the
parameter's own delta.  `xset` `LM_DELTA_ESCALATE` `off`
restores the old behaviour.

**migrad**

**Syntax:** `method` migrad [<# of eval>]
  [<minuit strategy>] [<minuit tolerance>]

The Minuit2 migrad method. `<# of eval>` is the number of function 
evaluations to perform before giving up. Migrad uses an internal 
convergence criterion. `<minuit strategy>` takes values 0, 1, or
2 with 0 the fastest method but with lowest reliability and 2 the
slowest method with highest reliability. The default is
2. The fit will stop when the estimated difference between the current
fit statistic and the minimum is less than `<minuit tolerance>`
times 0.001. The default tolerance is 0.1.

Migrad is given the first derivatives of the statistic by XSPEC, analytic
where the model allows it as for leven.  Under the default
`xset` `ANALYTIC_GRAD` `auto` it keeps the analytic
gradient of table models, which leven replaces by finite differences,
because migrad stops when the gradient it is given is close to zero, and a finite-difference gradient of a table model can be close to zero short of the minimum.  With
`never`, or `DISABLE_ANALYTIC_GRAD` `yes`, migrad
fits of such models can stop early; check them with leven.

The current version of Minuit2 included is that from ROOT v5.34. Documentation
on Minuit2 can be found at http://seal.web.cern.ch/seal/MathLibs/Minuit2/html/.

**Parameter limits and the Minuit methods.** Both Minuit methods work in
the parameter's value directly, and *soft limits have no effect on them*.
Where a hard limit is passed to Minuit, Minuit enforces it by minimizing in an
internal coordinate of its own: for a parameter bounded on both sides the
external value $P$ is related to the internal one $P_{\rm int}$ by

$P = P_{\rm min} + \frac{1}{2}(P_{\rm max}-P_{\rm min})(\sin P_{\rm int} + 1)$

and by a square-root relation for a parameter bounded on one side only. Minuit
applies the Jacobian of this transformation to the gradient and to the
covariance matrix itself, so both the fit and the reported uncertainties are in
the coordinate you asked for.

The cost is resolution. The internal coordinate covers the whole allowed range
over an interval of order unity, so the wider the range between the hard
limits, the less of the external parameter each internal step can resolve. A
range far wider than the region the parameter can plausibly occupy therefore
degrades the minimization and, more visibly, the uncertainties Minuit reports
from its error matrix. This is Minuit's own advice as well: do not use limits
you do not need, and where you do need them, make them tight.

XSPEC passes a parameter's hard limits to Minuit only when they span a range of
100 or less; a parameter whose hard limits are wider than that -- which
includes every normalization, whose default hard maximum is $10^{24}$ -- is
given to Minuit unbounded. Such a parameter is still confined to its hard
limits, because XSPEC clamps it there, but outside them Minuit sees a flat
statistic rather than a boundary.

The practical advice when fitting with `migrad` or `simplex` is
therefore to set the hard limits of the free parameters explicitly, with
`newpar`, to a range the parameter can plausibly take -- for a
normalization known to within a few orders of magnitude, say, a range of $10$
rather than $10^{24}$ -- and to check afterwards that no parameter has ended up
against a limit you imposed. Soft limits will not restrain a Minuit fit, and
the reported uncertainties are only as good as the range Minuit was given.

If migrad is still not working well, try `fit` `global` or a
different starting point; a fit that reports convergence with a parameter
pegged at a limit has usually not converged at all.

A Minuit fit can end short of the minimum in two ways, and neither is visible
in the parameter values it leaves behind, so XSPEC reports both. The test in
each case is the estimated distance to the minimum (edm) --- Minuit's own
estimate of how far in fit statistic the current point is from the minimum ---
against the criterion Minuit converges on, which is 0.002 times the tolerance.

The first is running out of function evaluations. This is ordinary, and
continuing is simply another `fit`:

```
***Warning: migrad stopped at its limit on function evaluations, with an
 estimated distance to the minimum of 1.86779 against a convergence
 criterion of 0.0002.  It has not converged.
 Fit again to continue from this point, or raise the number of evaluations
 in the method command.
```

The second is Minuit stopping of its own accord, when the error matrix it
carries between iterations yields no direction of improvement. Fitting again
from that point will do the same thing, so the remedy is different:

```
***Warning: migrad did not converge.  Minuit found no direction of
 improvement from this point, with an estimated distance to the minimum
 of 3306.74 against a convergence criterion of 0.0002.
 The parameter values below are where it stopped and may not be the minimum.
```

A fit that ends either way has not been minimized to Minuit's own satisfaction,
whatever the parameter values look like. Note that the edm is an estimate made
from the error matrix, so a fit that has in fact reached the minimum can still
report a value above the criterion; what the warning tells you is that Minuit
stopped for a reason other than convergence.

**simplex**

**Syntax:** `method` simplex [<# of evaluations>]
  [<minuit strategy>] [<minuit tolerance>]

The Minuit2 simplex method.  <# of evaluations> is the number of
function evaluations to perform before giving up. Simplex uses an
internal convergence criterion. `<minuit strategy>` takes values
0, 1, or 2 with 0 the fastest method but with lowest reliability and 2
the slowest method with highest reliability. The default is
2. The fit will stop when the estimated difference between the current
fit statistic and the minimum is less than `<minuit tolerance>`
times 0.001. The default tolerance is 0.1.

This method is included for historical interest and is almost always
outperformed by migrad.

**global**

**Syntax:** `method` global [<maxgen> [<popsize>]]

The derivative-free Differential Evolution (DE) global optimizer.  Unlike
`leven`, `migrad`, and `simplex` --- which are
*local* optimizers that descend to the nearest minimum from the current
parameter values --- `global` searches the full soft-limit
(``min''/``max'') box of every thawed parameter using only statistic
evaluations, so it can cross barriers between local minima and works for the
entire model library, including local models that provide no analytic
gradients.  `<maxgen>` sets the number of DE generations (default 200)
and `<popsize>` the population size (default automatic,
$\mathrm{clamp}(10D, 15, 200)$ for $D$ thawed parameters, and never fewer
than 4); these are the only tunable controls.  The search is reproducible
under `xset seed`, and its likelihood batch can be spread over $N$
processes with `parallel global` <N>.

In most cases you do *not* select this method directly.  The recommended
way to use the global search is the `fit` `global` command, which
runs a DE sweep as a *preconditioner* and then polishes the best point it
finds with your local method (`leven`, `migrad`, or
`simplex`) --- combining DE's global reach with a local optimizer's
accurate final statistic, parameter errors, and covariance, and adding
never-regress protection and competitive-basin reporting.  Selecting
`method` `global` instead makes *every* subsequent
`fit` a bare DE search with no local polish, which is coarser and rarely
what you want.  `improve` is the warm-restart form of the same DE
machinery.  See `fit` `global` for a full description of the
global search, its behaviour on wide-range parameters, and its output.
