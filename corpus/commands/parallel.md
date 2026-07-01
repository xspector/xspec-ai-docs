---
name: parallel
aliases: [xparallel]
also_documents: [parallelleven, parallelwalkers, parallelhmc, parallelnest, parallelglobal, parallelsim]
source: XSparallel.tex
---

# parallel

**enable parallel processing for particular tasks in XSPEC.**

**Syntax:** `parallel` <task>   <max num of processes>

where `<task>` is currently limited to `leven`, `global`, `error`, `steppar`,
`goodness`, `walkers`, `hmc`, or `nest`.  For best results,
it is recommended that you set `<max num of processes>` to the number of CPU cores on your machine.
Set `<max num processes>` back to 1 to turn parallel processing off for the particular task.
To display current settings, type 'parallel' with no arguments.

The `leven` option will spawn up to `<max num>` processes during the Levenberg-Marquardt fitting,
specifically to perform the N independent calculations of the parameter first-order
partial derivatives (N being the number of variable fit parameters).

The speed-up that one can expect is highly dependent upon the model in use.
For simpler models with quick calculation times, you will probably see little
to no speed gain with `parallel leven`.  But with multi-core CPUs, gains should
be quite noticeable when the model calculation consumes a large fraction of the
overall fitting time.  For example, with fits using the time-intensive `sedov` model
on a 4-core machine, we've typically seen about a 40% reduction in fit time
compared with the single processing case.

The `error` option is for running parallel computations within XSPEC's `error` command.
This enables the error calculations for multiple parameters to be performed simultaneously.
The speed-up here should simply be proportional to the number of cores available.
However for cases where complications are reported (such as a new minimum found,
or a non-monotonicity in the statistic space), it is recommended that you perform
the error calculations in standard single-process mode.

When the `steppar` option is set, XSPEC will divide the N-dimensional steppar grid into 
`<max num>` sections of equal size, and spawn a separate process for calculating each section.

If both `parallel` `leven` and `error` or `steppar`
are in use, XSPEC will temporarily disable the lower-level`leven`
parallelization when running the higher-level parallel `error`
or `steppar` command calculations.

The `goodness` option is for parallelizing the calculations of the
simulated spectra during a `goodness` command run.

The `walkers`
option may be used to speed up the calculation of sets of `walkers`
needed for Monte Carlo Markov Chain runs using the Goodman-Weare algorithm
(see `chain`).

The `hmc` option controls concurrency for the `hmc` command.
Each `hmc` chain is run in its own sub-process when
`parallel hmc` `<N>` is set to $N \geq 2$; with the default
`1` all chains are run back-to-back in the parent process, which
is fine for production sampling but does not give an honest Rubin--Gelman
$\hat{R}$ because the chains are seeded sequentially from a single RNG
stream.  Set `hmc` to the number of `hmc` `chains`
for parallel sampling with independent seeds.

The `nest` option enables a worker pool for the `nest`
command.  With `parallel nest` `<N>` set to $N \geq 2$,
the nested sampler dispatches the likelihood-restricted prior
draws across $N$ subprocesses; speed-up is sub-linear (the
ellipsoid update is serial) but typically a factor of 2--3 on a
four-core host.

The `global` option spreads the Differential
Evolution search of `fit global` (and `improve`) across
`<N>` subprocesses, which evaluate the statistic for the trial
population in parallel.  As with `leven`, set it to roughly the
number of physical cores; the global-search result is unchanged
(bit-identical and reproducible under `xset seed`), only faster.

The `sim` option distributes the realizations of
the `sim` command across `<N>` subprocesses.  The parameter sets are
drawn in the parent process before the work is dispatched, so the results are
identical (and reproducible under `xset seed`) whether the run is
serial or parallel; only the per-realization counting noise differs.

**Examples:**

```
XSPEC12> model cflow
// Using a model with 5 variable fit parameters.

XSPEC12> parallel leven 4
XSPEC12> fit
// Calculations for the 5 parameters will be divided amongst
//	4 processes during the fit.

XSPEC12> parallel leven 1
	// Restores single-process calculation to the
	//	Levenberg-Marquardt algorithm.

XSPEC12> parallel error 3
	// Allow up to 3 simultaneous 'error' parameter calculations
	//	to be performed in parallel.

XSPEC12> error 2 3 6
	// Perform error calculations on parameters 2, 3, and 6 in parallel.

XSPEC12> parallel steppar 4
      // The following 20x30 steppar grid will be split amongst
      // 4 parallel processes.
XSPEC12> steppar 1 10. 11. 20 2 .5 .8 30

	// Display current settings:
XSPEC12> parallel
Maximum number of parallel processes:
   error: 3
   goodness: 1
   leven: 1
   steppar: 4
   walkers: 1
```
