---
name: nest
aliases: [xnest]
also_documents: [nestrun, nestlive, nesttol, nestenlarge, nestclusters, nestresample, nestcheckpoint, nestseed, nestinfo, nestevidence]
source: XSnest.tex
---

# nest

**run a nested-sampling exploration**

**Syntax:** `nest` <subcommand> [<args>]

The `nest` command runs a multi-ellipsoidal nested sampler over
the currently-thawed model parameters.  Unlike `chain` and
`hmc`, nested sampling produces a sequence of *weighted*
posterior samples plus an estimate of the marginal likelihood (model
evidence) $\log Z$, computed by likelihood-restricted prior sampling
inside a contracting envelope of bounding ellipsoids.  See the
nested-sampling discussion in Chapter BayesianMethods for the
algorithmic background and Section BayesianExample for a
worked example.

`nest` requires proper, integrable priors on every thawed
parameter.  Parameters with default flat priors over a hard
range that spans more than four decades (typical of column densities
and normalisations) cause `nest` to refuse to start; in such
cases either narrow the parameter limits via `newpar` or assign
a Jeffreys prior via `bayes` `JEFFREYS` before invoking
`nest run`.  See Chapter BayesianMethods, Section 3, for
the available prior families.

`nest` does not warm-start from a fit -- it samples from the
prior and contracts inward.  A `fit` is therefore not required
before `nest run`, but it is useful for diagnosing the prior
choice: if the MLE lies in a region the prior assigns very low
probability the run will spend many iterations in the contraction
phase before finding the likelihood peak.

By default `nest` runs in a single process.  Set
`parallel nest` `<N>` to run with $N$ worker processes
sharing the likelihood-restricted sampling pool, which gives
sub-linear but significant speed-up.

- [`run` `<fileName>`]Executes the
sampler and writes the output to `<fileName>`.  The file
contains two FITS extensions: a `NEST` table with the weighted
nested samples and their log-likelihood / log-weight columns, and a
`CHAIN` table with equal-weight resampled draws compatible
with `chain` `load`.  Prefix the filename with
`!` to discard any existing checkpoint and overwrite.
Without the prefix, if a checkpoint file
`<fileName>.ckpt.fits` exists and is dimensionally compatible
with the current model, `nest run` resumes from the saved
iteration count.

- [`live` `<N>`]Number of live
points (the size of the contracting ellipsoid pool).  Default 400.
More live points give a finer-grained estimate of $\log Z$ and reduce
the chance of missing isolated modes, at proportional cost.
Conventional values run from 100 (cheap exploration) to 2000
(production-grade evidence for paper figures).

- [`tol` `<eps>`]Skilling
log-evidence termination tolerance.  Default 0.5.  Sampling stops
when the residual evidence in the live points falls below
`<eps>` times the accumulated total.  Smaller values run longer
and produce tighter $\log Z$ estimates.

- [`enlarge` `<factor>`]Enlargement factor applied to the volume of the bounding ellipsoids
before drawing new live points.  Default 1.2.  Larger values reduce
the chance of clipping the true iso-likelihood contour at the cost
of more sampling per replaced live point.

- [`clusters` `<K>`]Maximum
number of ellipsoids used to bound the live-point cloud.  Default 16.
Setting `1` forces the single-ellipsoid algorithm of Mukherjee
et al. (2006), which is faster but cannot follow multi-modal
posteriors; the default uses the X-means split heuristic to grow the
ellipsoid count up to the cap as needed.

- [`resample` `<N>`]Number of
equal-weight posterior draws to write to the `CHAIN`
extension.  Default 4000.  These are produced by importance
resampling from the weighted `NEST` table and are what
`chain` `load` will see if it is pointed at the output
file.

- [`checkpoint` `<N>`]Write a
checkpoint every `<N>` iterations.  Default 200.  Set
`0` to disable checkpoint writing.

- [`seed` `<N>`]Seed of the
sampler's own random stream.  Default `0`, which makes each
`nest run` draw a fresh seed; the seed used is printed at the
end of the run and reported by `nest info`, so a run made
this way can still be repeated afterwards by setting `seed` to
that value.  The seed covers the resampled `CHAIN` extension as
well as the sampler itself, so repeating a run reproduces the whole
output file.  Nested sampling does not draw from the generator
`xset` `seed` controls, so this setting is sufficient on
its own -- two runs with the same seed agree even if that generator
was disturbed in between.  Note that `parallel nest` `<N>`
partitions the sampling across workers, so reproducing a run also
requires the same worker count.

- [`info`]Print the current sampler
settings, and the seed the most recent run used.

- [`evidence`]Print the
$\log Z$ estimate and its uncertainty from the most recent run.

**Progress output:** every 100 iterations the sampler prints
the iteration count, the running $\log Z$, the likelihood of the
point just replaced (`worstL`), the information $H$, the
number of bounding ellipsoids in use (`K`), the sampling
efficiency over the interval since the previous line
(`eff`: points replaced per likelihood evaluation) and the
cumulative number of likelihood evaluations (`nlike`).  The
efficiency is the number to watch: it starts near one while the
ellipsoids still bound the whole prior and falls as the constrained
region contracts and the ellipsoids over-cover it.  A run whose
efficiency has fallen to $10^{-4}$ needs over ten thousand
evaluations per replaced point and will not finish in a useful
time; a warning is printed the first time this happens.  The usual
remedies are narrower parameter limits (the ellipsoids are fit in
the unit cube, so a decade of unused prior range is a decade of
wasted volume), a smaller `enlarge` factor, or
`clusters` `1` when `K` is seen to
oscillate between one and several ellipsoids on a single-mode
posterior.

**End-of-run summary:** when the run finishes it reports on the
answer, not only on the sampler.  The output file is loaded back in
automatically (as `chain` `run` has always done), and the
run then prints a verdict followed by a per-parameter posterior table.

The verdict judges the two jobs a nested sampling run does, because it
can pass one and fail the other.  It warns when the run stopped for any
reason other than reaching the $\Delta\log Z$ tolerance --- a run halted
by the iteration cap otherwise produces a finish line of exactly the same
shape as a converged one --- when the effective sample size falls below
400, and when the overall sampling efficiency falls below $10^{-4}$.  A
posterior with more than one mode is reported as information rather than
as a warning: multimodality is a property of the problem, but an
equal-tailed interval computed across two modes describes neither of
them, and the user needs to know that before reading the table.  The
$\log Z$ uncertainty is printed alongside $\sqrt{H/n_{\rm live}}$, the
value theory expects of it.

The effective sample size is Kish's $(\sum w)^2/\sum w^2$ over the
importance weights, and it is usually far smaller than the number of
points in the file.  It is reported at the run level rather than per
parameter because it depends only on the weights.  Note that a run with
few live points will trip the 400 threshold even when its evidence is
perfectly good; the threshold is about the posterior, not the evidence.

The table reports an equal-tailed credible interval for each variable
parameter, on exactly the convention `error` uses: the fit's
$\Delta$-statistic setting is converted to a percentage through the
$\chi^2$-with-one-degree-of-freedom equivalence, so the default 2.706
gives the 5th and 95th percentiles.  The same interval is what
`error` reports for a loaded chain, because it is the same
computation.  Central values and the weighted standard deviation come
from `chain` `stat` and `chain` `diag`.

The run does *not* move the model.  Parameter values are restored to
what they were before the run and no error bounds are written, so
`show` `par` still displays the covariance from the last
fit.  Use `chain set` to set the parameters from the
chain, or `error` to write the credible interval into them.

**Numbers from older files have changed:** `chain` `load`
now reads the `NEST` extension, which holds the importance-weighted
posterior, in preference to the `CHAIN` extension, which holds an
equal-weight resampling of it.  Both are still written, so scripts that
read the `CHAIN` extension directly are unaffected.  But
`error`, `margin`, `flux`, `lumin`,
`eqwidth`, `chain` `dic` and
`chain` `stat` will return slightly different values for
nest output files written by earlier versions, because they now use the
weights instead of a lossy re-encoding of them.  The load announces the
point count and the effective sample size so that a changed number can be
connected to its cause.

Everything the summary reports is also readable from a script
with `tclout` `nest` (Section tcloutnest), including the verdict and
the per-parameter credible intervals.

**Examples:**

```
XSPEC> newpar 1 0.05 0.001 1e-6 1e-6 100000 1e6
XSPEC> newpar 5 0.04 0.01  1e-30 1e-30 1e20 1e24
XSPEC> bayes on
XSPEC> bayes 1 JEFFREYS
XSPEC> bayes 5 JEFFREYS
XSPEC> parallel nest 4
XSPEC> nest live 400
XSPEC> nest run nest.fits
XSPEC> nest evidence
```

The `newpar` commands narrow the search ranges of the absorber
column and apec normalisation (otherwise their default 31-decade
ranges would cause `nest` to refuse to start), and the
`bayes` `JEFFREYS` commands switch them to log-uniform
priors so that the search proceeds over the full narrowed range
without favouring large absolute values.
