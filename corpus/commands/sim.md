---
name: sim
aliases: [xsim]
also_documents: []
source: XSsim.tex
---

# sim

**bulk posterior-predictive simulation**

Generate many simulated realizations of the loaded spectra, optionally
refit each one and run a command file on it, and accumulate the
results.  This is the in-program replacement for the common scripted
loop of `tclout` `simpars`, `newpar` and
`fakeit` (see the `multifake` script): it is faster, keeps
the whole random-number sequence under a single `xset`
`seed`, and can be run in parallel.

**Syntax:** `sim` <# of realizations> [fsigma <f>] [nostat] [fit]
  [@<cmdfile>] [outfile <name>]

For each realization, `sim` draws a set of parameter values,
evaluates the model, and replaces the loaded spectra (and their
backgrounds) in place with a simulated dataset.  Unlike `fakeit`,
no files are written and no datasets are created or destroyed -- the
realization occupies the spectra that are already loaded, and the
original data, model parameters and fit state are restored when the
command finishes.

The drawn parameter values, the test statistic of each realization, and
(with the `fit` option) the refit parameters and statistic, are
retained for retrieval with `tclout` `sim` (see below).

The options are:

- [`fsigma <f>`] Scale of the parameter draws.  The
values are drawn from a multivariate Normal distribution centered on
the best fit with covariance $f^2 C$, where $C$ is the fit covariance
matrix (the same mechanism as `tclout` `simpars`).  The
default is `f`=1.  Setting `f`=0 fixes the parameters at
their current values for every realization, so that only the counting
statistics vary (useful for frequentist coverage studies and for
isolating shot noise from parameter uncertainty).  Values greater than
1 deliberately broaden the draws.  When MCMC chains are loaded and
synchronized with the fit parameters, the draws are taken directly from
the chains and `fsigma` is ignored.

- [`nostat`] Realize the expected (noise-free) model counts
instead of adding counting statistics.  Combined with `fsigma 0`
this produces a fully deterministic dataset equal to the current model.
(`nostat` also suppresses the correlated draw described below.)

- [`fit`] Refit the model to each realization before
recording its statistic (a parametric bootstrap).  The refit parameter
values and statistic are then available through `tclout`
`sim fitpars` and `sim fitstat`.

- [`@<cmdfile>`] Run the XSPEC command file
`<cmdfile>` once on every realization, after the optional refit.
The script may interrogate the realization with any XSPEC command
(`flux`, `tclout`, a further `fit`, and so on).  The
following Tcl variables form the contract between `sim` and the
script:

- [`$xspec_simiter`] (input) the 1-based index of the
current realization, unique across all parallel processes.

- [`$xspec_simresult`] (output) a flat Tcl list of real
numbers that the script sets; these are collected, one row per
realization, and retrieved with `tclout` `sim result`.

- [`$xspec_simfile`] (input) a filename the script may
append free-form output to.  Use this rather than a hardcoded name: in
a parallel run each process is given a private file, which
`sim` concatenates in realization order at the end (see
`outfile`).

If the script raises an error on any realization, the entire run is
aborted, no output file is produced, and the original state is
restored.  The script must not add or remove spectra or redefine the
model.

- [`outfile <name>`] The file that
`$xspec_simfile` points to.  In a serial run the script
appends directly to `<name>` (so it may be watched as it grows);
in a parallel run each process writes a private temporary that is
concatenated, in realization order, into `<name>` when the run
completes.  This option has no effect unless an `@<cmdfile>`
script is also supplied.

The results of the most recent `sim` command are obtained with
the `tclout` `sim` options:

- [`tclout sim n`] the number of realizations.

- [`tclout sim stat`] the test statistic of each realization.

- [`tclout sim pars <i>`] the drawn parameter values of
realization `<i>` (1-based).

- [`tclout sim fitstat`] the refit statistic of each
realization (`fit` runs only).

- [`tclout sim fitpars <i>`] the refit parameter values
of realization `<i>` (`fit` runs only).

- [`tclout sim result <i>`] the
`$xspec_simresult` list harvested from the script for
realization `<i>`.

The simulation may be spread over several processes by setting the
`parallel` command's `sim` option.  The parameter sets are
all drawn up front by the parent process, so the drawn values (and
their order) are reproducible from the `xset` `seed` and
are identical whether the run is serial or parallel; only the
per-realization counting noise differs between a serial and a parallel
run, as for the `goodness` command.

When the loaded spectra form a covariance group fit with
`statistic` `chistokes` or `chicov`, each
realization draws the group's members jointly from the per-bin
cross-spectrum covariance, so the simulated test statistic follows the
correct distribution; see the correlated-spectra discussion in the
Statistics appendix.

**Example:** accumulate the fit parameters and a flux measurement
from 1000 bootstrap realizations, four processes at a time.  The
command file `boot.xcm` contains

```
flux 0.5 10.0
tclout flux 1
scan $xspec_tclout "%f" f
tclout param 1
scan $xspec_tclout "%f" p1
set xspec_simresult [list $p1 $f]
```

and is driven by

```
XSPEC12> parallel sim 4
XSPEC12> xset seed 1234
XSPEC12> sim 1000 fit @boot.xcm outfile boot.txt
```

After the run, `boot.txt` holds 1000 rows of the photon index
and flux, and the same rows are available individually through
`tclout` `sim result`.
