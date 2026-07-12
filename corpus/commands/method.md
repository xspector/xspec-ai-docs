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
  [<crit beta>]] [delay | nodelay]

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

`<# of eval>`, `<crit delta>`, `<crit beta>`, `delay`, 
and `nodelay` may also be set through the `fit` command.

This method requires an estimate of the second derivative of the statistic 
with respect to the parameters. By default, XSPEC calculates these using 
an analytic expression which assumes that partial 2nd derivatives of the 
model with respect to its parameters may be ignored.  This may be changed 
by setting the USE_CHAIN_RULE flag to `false` in the user's 
startup Xspec.init initialization file.  XSPEC will then calculate 
all second derivatives numerically, which can be noticeably slower.

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

The current version of Minuit2 included is that from ROOT v5.34. Documentation 
on Minuit2 can be found at http://seal.web.cern.ch/seal/MathLibs/Minuit2/html/.

If migrad is not working well try experimenting with different hard and soft 
limits on parameters.

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
