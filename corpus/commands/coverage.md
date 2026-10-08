---
name: coverage
aliases: [xcoverage]
also_documents: []
source: XScoverage.tex
---

# coverage

**how often confidence or credible intervals contain the truth**

Measure the frequentist coverage of the intervals `error` (or a
`chain`) gives, for data like the data loaded, by simulation.

**Syntax:** `coverage` <# of simulations> [`<parameters>`]
  [method error| chain] [level `<value>`] [file `<name>`]

The current parameter values are taken as the truth --- normally the best
fit, but any values will do.  `<# of simulations>` datasets are
simulated from the model at those values, as `goodness` simulates
them (through each spectrum's own response and exposure, with counting
statistics appropriate to the fit statistic, and the background
included).  Each simulated dataset is refitted, starting from the truth,
and the interval of each tested parameter is found:

- [`method error`] (the default) the `error` search at the
  level's $\Delta$-statistic.  The search's limit on the reduced
  statistic does not apply: a simulation is never dropped for fitting
  badly, since those are the simulations most likely to miss.

- [`method chain`] a chain run with the current `chain`
  settings (from the fit's covariance, as `chain run` starts), and
  its central credible interval at the level's probability.  XSPEC prints
  the total number of chain steps and asks before starting, unless
  `query yes` is in force.  Refused while chains are loaded:
  `chain unload` them first.

For each parameter the report gives the truth, the fraction of intervals
containing it with its binomial $1\sigma$ error, and the fractions of
intervals lying wholly *below* and wholly *above* the truth ---
an interval that is right on average but shifted shows up as unbalanced
misses.  A fraction more than $3\sigma$ (of the nominal rate) from the
nominal rate is marked.  The *Flagged* column counts intervals the
search flagged (pegged at a hard limit, non-monotonic, or failed in one
direction); they are counted like the others.  *Failed* counts
simulations that gave no interval at all, which are left out of the
fractions.

`<parameters>` is a list of parameter numbers and ranges as
`error` takes them (`2`, `1-3`, `mod:2`); the
default is every variable model parameter.  `level` is a
probability between 0 and 1, converted to the one-parameter
$\Delta$-statistic (0.9 gives 2.706), or a $\Delta$-statistic of 1 or
more; the default is the $\Delta$ `error` is using.  `file`
writes one row per simulation: the simulation number, its refitted
statistic, and for each parameter the truth, the refitted value, the
interval and the `error` flag string.

The parameter values, their error bounds, the covariance matrix, the
loaded data and whether the fit is current are all as they were
afterwards.  Each simulation draws from a random stream of its own,
derived from the random seed, so a run is reproduced by
`xset seed` and `parallel coverage` `<n>` spreads
the simulations over processes without changing any result.  Inside a
simulation every other task runs in a single process.  The results can be
read with `tclout coverage`.

**Examples:**

```
XSPEC> fit
XSPEC> parallel coverage 4
XSPEC> coverage 1000
// How often error's 90% intervals (delta 2.706) contain the
// best-fit values, for every variable parameter.
XSPEC> coverage 500 3 level 0.68 file cov.txt
// Parameter 3 only, 1-sigma intervals; one row per simulation
// written to cov.txt.
XSPEC> chain length 10000
XSPEC> coverage 200 method chain
// The same question for chain credible intervals.
```
