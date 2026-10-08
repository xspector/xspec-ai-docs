---
name: hmc
aliases: [xhmc]
also_documents: [hmcrun, hmcsamples, hmcwarmup, hmcchains, hmcstepsize, hmcmaxdepth, hmctargetaccept, hmcdivergencethreshold, hmcadapt, hmccheckpoint, hmcinfo]
source: XShmc.tex
---

# hmc

**run a Hamiltonian Monte Carlo (NUTS) chain**

**Syntax:** `hmc` <subcommand> [<args>]

The `hmc` command runs a No-U-Turn-Sampler variant of
Hamiltonian Monte Carlo over the currently-thawed model parameters,
using the analytic posterior gradient described in
Appendix AppendixAlgorithmsVJP.  Unlike `chain`, which steps
the chain via Metropolis--Hastings or Goodman--Weare proposals,
`hmc` integrates Hamiltonian trajectories with leap-frog steps
adapted to the local posterior curvature.  This is typically more
sample-efficient than `chain` on smooth, moderate-dimensional
posteriors but each step is more expensive because every leap-frog
sub-step requires one gradient evaluation.

`hmc` does not require every component to be gradiented.  A fully
gradiented model uses the fast reverse-mode (VJP) gradient; if one or
more additive or multiplicative components lack a registered gradient
their parameters are finite-differenced on the statistic while the rest
stay analytic (the same per-column hybrid used by `fit`).  It
refuses to start only on a hard structural reject --- an ungradiented
convolution component, or a mixing (`mix`, `amx`) model
--- in which case the user is asked to fall back to `chain`.

A `fit` should be performed before `hmc run` so the
starting point is at or near the maximum-likelihood estimate; the
warmup phase then adapts the leap-frog step size and the diagonal mass
matrix.  See the discussion of HMC in Chapter BayesianMethods
and the worked example in Section BayesianExample for context
and example output.

By default `hmc` runs all chains back-to-back in the parent
process.  To run them in parallel as separate sub-processes
(necessary for an honest Rubin--Gelman $\hat{R}$ diagnostic, see
`chain` `stat`), set `parallel hmc` `<N>`
to the number of chains before invoking `hmc run`.

- [`run` `<fileName>`]Executes the
sampler and writes samples to `<fileName>` as a FITS table
compatible with `chain` `load`.  Prefix the filename
with `!` to discard any existing per-chain checkpoint and
overwrite the output file.  Without the prefix, if checkpoint files
`<fileName>.chain<C>.ckpt` exist from an earlier interrupted
run and are dimensionally compatible with the current model,
`hmc run` resumes those chains from the saved sample index
(skipping warmup), and the checkpoints are deleted on successful
completion.

- [`samples` `<N>`]Number of
post-warmup samples per chain.  Default 1000.

- [`warmup` `<N>`]Number of warmup
samples per chain.  Default 1000.  During warmup the leap-frog step
size is adapted by dual-averaging and the diagonal mass matrix is
fit from sample variance; both freeze at the end of warmup and are
held fixed for the production samples.

- [`chains` `<N>`]Number of
independent chains to run.  Default 4.  Chains share the model and
starting point but use distinct RNG streams.  Concurrency is gated
by `parallel hmc`; with the default
`parallel hmc` `1` the chains run back-to-back in the
parent process, which is suitable for production sampling but not
for $\hat{R}$ (because chains are seeded sequentially rather than
independently).

- [`stepsize` `<eps>`]Initial
leap-frog step size.  Default 0.05.  Adapted by dual-averaging
during warmup; if `adapt` is `off` the user value is
held fixed throughout.

- [`maxdepth` `<K>`]Maximum
depth of the NUTS tree-doubling recursion.  Default 10.  A trajectory
of depth $K$ corresponds to up to $2^K$ leap-frog sub-steps, so the
default caps the per-sample cost at 1024 gradient evaluations.
Setting this lower trades sampling quality for speed.  The number of
trajectories that have hit the cap is the `capped` count on
the progress lines.

- [`target_accept` `<X>`]Target Metropolis acceptance probability for the dual-averaging
adaptation.  Default 0.8 (Stan default).  Raise toward 0.95 for
posteriors with strong curvature variation where the default rate
produces divergent transitions; expect a smaller step size and a
higher per-sample cost.

- [`divergence_threshold` `<X>`]Hamiltonian-energy error above which a trajectory is flagged as
divergent and discarded.  Default 1000.  Divergent transitions
indicate the leap-frog integrator is breaking the symplectic
guarantee of HMC, usually because the step size is too large for the
local curvature.  The total divergent count is printed at the end of
a run; if it exceeds a few percent of the post-warmup samples the
posterior should be reparameterised or `target_accept`
raised.

- [`adapt` `on`|`off`]Enables (default) or disables warmup adaptation of step size and
mass matrix.  With `off` the sampler runs at the user-set
`stepsize` with an identity mass matrix; useful for
controlled experiments and reproducing earlier runs.

- [`checkpoint` `<N>`]Write a
per-chain checkpoint every `<N>` samples.  Default 200.  Set
`0` to disable checkpoint writing (and therefore resume).

- [`info`]Print the current sampler
settings, the divergent count from the most recent run if any, and
mean Metropolis acceptance.

**Progress output:** at chatter $\geq 10$ each chain prints a
line every 100 iterations of its warmup and sampling phases, and in
any case whenever a minute has passed since its last line, so a run
whose single iteration is expensive still reports.  The line gives
the chain id (the `CHAINID` value in the output file), the
phase and its iteration count, the log posterior of the current
sample, the current step size `eps`, the tree depth and
number of leap-frog steps of the last trajectory, its mean Metropolis
acceptance, and three cumulative counts: divergent trajectories,
trajectories that ran to `maxdepth` without a U-turn
(`capped`), and gradient evaluations (`grads`).  A
run that looks stalled is usually one whose trajectories are all
capped: every such iteration costs $2^K-1$ gradient evaluations, and
if this persists past the first few hundred warmup iterations the
mass matrix has not found the parameter scales, which a `fit`
before the run (to set the parameter deltas) normally cures.  The
end of warmup prints the frozen step size and the range of the
mass-matrix diagonal.

**End-of-run summary:** the run loads its output file back in and
prints a verdict and a per-parameter posterior table, in the same form
`nest` uses.

Because an HMC chain is a genuine Markov chain, the verdict is the
ordinary chain diagnostic --- split-$\hat{R}$, bulk and tail effective
sample size, and the integrated autocorrelation time, on the same
thresholds `chain` `diag` applies --- together with the
divergent-transition count, which the table does not carry.  A divergence
means the integrator could not follow the posterior's geometry at that
point, and the region around it is under-explored.

The table is deliberately identical to the one `nest` prints: an
equal-tailed credible interval per variable parameter, on the convention
`error` uses.  The two samplers differ in how the sample was
produced, and that difference belongs in the verdict rather than in the
shape of the answer.

As with `nest`, the run does not move the model: parameter values
are restored and no error bounds are written.  Use
`chain set` or `error` to act on the result.

Everything the summary reports is also readable from a script
with `tclout` `hmc` (Section tclouthmc), including the verdict and
the per-parameter credible intervals.

**Examples:**

```
XSPEC> fit
XSPEC> parallel hmc 4
XSPEC> hmc warmup 1000
XSPEC> hmc samples 1000
XSPEC> hmc chains 4
XSPEC> hmc run mychain.fits
```

The samples are written to `mychain.fits` in a format
compatible with `chain` `load`, so subsequent
`error`, `flux` and `eqwidth` commands can use them
as the parameter-distribution source.
