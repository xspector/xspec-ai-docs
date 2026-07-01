---
name: nest
aliases: [xnest]
also_documents: [nestrun, nestlive, nesttol, nestenlarge, nestclusters, nestresample, nestcheckpoint, nestinfo, nestevidence]
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

- [`info`]Print the current sampler
settings.

- [`evidence`]Print the
$\log Z$ estimate and its uncertainty from the most recent run.

**Examples:**

```
XSPEC12> newpar 1 0.05 0.001 1e-6 1e-6 100000 1e6
XSPEC12> newpar 5 0.04 0.01  1e-30 1e-30 1e20 1e24
XSPEC12> bayes on
XSPEC12> bayes 1 JEFFREYS
XSPEC12> bayes 5 JEFFREYS
XSPEC12> parallel nest 4
XSPEC12> nest live 400
XSPEC12> nest run nest.fits
XSPEC12> nest evidence
```

The `newpar` commands narrow the search ranges of the absorber
column and apec normalisation (otherwise their default 31-decade
ranges would cause `nest` to refuse to start), and the
`bayes` `JEFFREYS` commands switch them to log-uniform
priors so that the search proceeds over the full narrowed range
without favouring large absolute values.
