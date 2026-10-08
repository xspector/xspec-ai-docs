---
name: cgof
aliases: [xcgof]
also_documents: []
source: XScgof.tex
---

# cgof

**C-statistic goodness of fit with model systematics**

**Syntax:** `cgof` [`f` <fraction>] [`draws` <n>]

**Syntax:** `cgof delta` <deltaC> <k> [`f` <fraction>] [`mu` <counts>]

For a fit under `statistic` `cstat` --- with no background,
or with a Poisson background (the W statistic) --- `cgof` reports
how well the model fits, with or without an allowance for systematic
errors in the model.  It is a report on the current fit: nothing is
refitted and nothing is changed.

Without arguments the command prints the exact expected value $E[C]$ and
standard deviation of the statistic under the fitted model, the
one-sided $p$-value of the fit's $C$ against them, and the relative
systematic error $\hat f$ that would account for the excess of $C$ over
$E[C]$ with its 68% interval.  With `f` `<fraction>` it also
prints the test with the systematics term added, so that a known
calibration uncertainty (say $2\%$, given as `f` `0.02`)
can be folded into the verdict.  The output looks like

```
 C-statistic goodness of fit with model systematics
 (Kaastra 2017, A&A 605, A51; Bonamente, Chen & Zimmerman 2025, ApJ 980, 139)
  spectrum   bins      counts       C     E[C_i]   Var[C_i]  background
         1    256     4502.84  322.82    267.276     542.83  Poisson, rate from 34 super-bins; 22.6% at the floor

  C = 322.82 over N = 256 bins with m = 3 free parameters (N - m = 253)
  without systematics:  E[C] = 264.276  sd = 23.17  (C - E)/sd = +2.53  p = 0.006
  implied relative systematic:  f = 11.8 %  (68 %: 8.4 % - 14.4 %)
  with f = 2 %:  mu_C = 1.688  sigma_C = 2.607  E[C_sys] = 265.964  sd = 23.32  (C - E)/sd = +2.44  p = 0.007
```

The moments of $C$ are those of Kaastra (2017): for each bin the
expectation and variance of its contribution to $C$ are summed exactly
over the Poisson distribution of the counts at the fitted model, so that
in the large-count limit $E[C_i]\to1$ and ${\rm Var}[C_i]\to2$ while for
sparse bins both fall well below the chi^2 values.  With a Poisson
background the sum runs over both the source and the background counts of
the bin with the profiled background rate solved for on every lattice
point, the true background rate being estimated by pooling the loaded
background to about 25 counts per super-bin (exactly as the `bias`
command does); the table says how many super-bins that produced and what
fraction of the bins sit at the background floor.  The fit's reduction is
then applied, $E[C]=\sum_iE[C_i]-m$ and ${\rm Var}[C]=\sum_i{\rm
Var}[C_i]-2m$ for $m$ free parameters, which reproduces the chi^2\
values $N-m$ and $2(N-m)$ in the large-count limit.  The $p$-value takes
$C$ to be normally distributed, which Kaastra finds adequate above about
30 counts in the whole spectrum.  This line alone --- the report at $f=0$
--- is the analytic goodness-of-fit test for `cstat` that SPEX
prints after every fit; XSPEC's `goodness` command remains the
Monte Carlo alternative.

The systematics model is that of Bonamente, Chen & Zimmerman (2025).
After the fit the model's predicted counts in each bin, $\hat\mu_i$, are
treated as a random variable with mean $\hat\mu_i$ and relative scatter
$f$, the same in every bin and independent between bins.  The statistic
then becomes $C_{\rm sys}=C+Y$ with $Y$ normal, of mean
$\mu_C=\sum_i\hat\mu_if^2$ and variance $\sigma_C^2=4\mu_C+2\sum_i\hat\mu_i^2f^4$
(the second term is not negligible: at the paper's own case it is 13% of
$\sigma_C^2$), so that the verdict with systematics compares $C$ with
$N(E[C]+\mu_C,\,{\rm Var}[C]+\sigma_C^2)$.  The best fit is the same
whether or not systematics are included; that is the point of the
method.  Because the systematic is a property of the model, with a
Poisson background it is placed on the source model only: a bin whose
predicted counts are $t_s(y_i+\hat f_i)$ carries the relative scatter
$f\,y_i/(y_i+\hat f_i)$, so the background counts, which are measured
rather than predicted, carry none.  Conversely the implied systematic
$\hat f$ is the value of $f$ for which $E[C_{\rm sys}]$ equals the
measured $C$, $\hat f^2=(C-E[C])/\sum_i\hat\mu_i$, and its interval is
where $C$ sits one standard deviation of $C_{\rm sys}$ from that
expectation; it is quoted only when $C>E[C]$, and otherwise the report
says no systematic is required and gives the upper bound alone.  The
method assumes bin-independent relative systematics of at most about
$10\%$: a larger disagreement between model and data is a failure of the
model, not a systematic.  This is also how `cgof` differs from the
`systematic` command, which adds a model fraction to the data
variance for chi^2 and changes the fit.

**Nested components.** `cgof` `delta` is a
calculator, like `ftest`, for the significance of a nested model
component (a line, an extra continuum) when systematics are present
(Bonamente, Zimmerman & Chen 2025).  Given the measured $\Delta C$ ---
$C$ of the fit without the component minus $C$ with it, both fitted
under `cstat` --- and the number $k$ of parameters the component
adds, it prints the nominal $p$-value of a chi^2 with $k$ degrees
of freedom and the $p$-value of $\Delta C_{\rm sys}=\Delta X+\Delta Y$,
where $\Delta X\sim\chi^2_k$ and $\Delta Y$ follows the Bessel
distribution $K_0(\alpha)$, the distribution of $\alpha Z_1Z_2$ for two
independent standard normals, with $\alpha=2f\sqrt{k\mu}$.  Here $\mu$ is
the model counts per bin where the component acts (`mu`); when it
is not given the mean model counts per noticed bin of the current fit is
used and the report says so.  The distribution of the sum, the
randomized chi^2 $R(k,\alpha)$, is evaluated as the exact
convolution of the two assuming they are independent, which the paper
validates in the tail that matters for a detection claim ($p\le0.1$).
One-sided critical values of $R(k,\alpha)$ at $q=0.1$, $0.05$, $0.01$ and
$0.001$ are printed beside the chi^2 ones.  The correction is
substantial: for the paper's case, $\Delta C=6.6$ with $k=1$ and about
700 counts per bin, the nominal $p=0.010$ becomes $0.041$ for a $5\%$
systematic.

**Pooled backgrounds.** With a background pooled by
`group` `back` the moments of a super-bin have no closed form
and are averaged over Monte Carlo realizations of its counts,
`<n>` per super-bin (default 2000), drawn from XSPEC's random
generator: `xset` `seed` immediately before the command
reproduces the run, and the report quotes the Monte Carlo uncertainty on
$E[C]$.  With an ungrouped background nothing is drawn.

`cgof` requires a valid `fit` first, and is refused for any
spectrum whose statistic is not `cstat` (for `chi` use the
`systematic` command; `pgstat` and `lstat` have no
exact expected statistic), for a non-Poisson background, and while
`bayes` is on (the statistic then carries prior terms).  Several
spectra in a joint fit are handled together and listed one per line.
The results of the last `cgof` and `cgof` `delta` can
be retrieved with `tclout` `cgof`, and PyXspec has
`Fit.cgof()` and `Fit.cgofDelta()`.  The moments are
described in Appendix AppendixStatistics.

**Examples:**

```
XSPEC> data src.pha
XSPEC> statistic cstat
XSPEC> model phabs(powerlaw)
XSPEC> fit
XSPEC> cgof
// expected C and its sd, the p-value of the fit, the implied systematic
XSPEC> cgof f 0.03
// the same, plus the verdict allowing a 3% model systematic
XSPEC> tclout cgof sys
// f mu_C sigma_C E[C_sys] sd (C-E)/sd p, for the 3% run
XSPEC> cgof delta 6.6 1 f 0.05 mu 700
// significance of a one-parameter component with Delta C = 6.6 at 5%
XSPEC> group back auto
XSPEC> fit
XSPEC> xset seed 4321
XSPEC> cgof draws 4000
// the pooled fit, 4000 Monte Carlo draws per super-bin, reproducible
```
