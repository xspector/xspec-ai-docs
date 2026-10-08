---
name: parallel
aliases: [xparallel]
also_documents: [parallelleven, paralleltotal, parallelwalkers, parallelhmc, parallelnest, parallelglobal, parallelsim, paralleltempering, parallelcoverage, parallellrt, paralleltiming]
source: XSparallel.tex
---

# parallel

**enable parallel processing for particular tasks in XSPEC.**

**Syntax:** `parallel` <task>   <max num of processes>

**Syntax:** `parallel` total  <N | auto | off>

where `<task>` is currently limited to `leven`, `global`, `error`, `steppar`,
`goodness`, `walkers`, `hmc`, `nest`, `sim`, `tempering`, `coverage`, or `lrt`.  For best results,
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

Only finite-difference derivatives are calculated in the subprocesses.
Derivatives of components with analytic gradients (see `xset`
`ANALYTIC_GRAD`) are calculated in the main process, which starts
the subprocesses on their finite differences first and works on the analytic
derivatives meanwhile.  Each subprocess keeps its own copy of the model:
once per derivative calculation it recalculates the components whose
parameters have changed, then recalculates only the perturbed component for
each derivative, as the main process does.  The derivatives are dealt out by
how long each took last time, longest first, and the main process takes a
share itself, typically the most expensive derivative, since it already has
the model calculated.  The results are identical to a single-process fit.
Because of this `leven` `<max num>` is a ceiling: with `xset`
`LEVEN_PARALLEL auto` (the default) each fit times its first set of
derivatives in the main process and, if that leaves room for a gain, its
second in parallel, and uses the subprocesses only if they were more than
10% quicker, checking again every 20 iterations; `forced` always
uses them.  The parallel timing includes starting the subprocesses, spread
over the number of derivative sets a pool has served on average, so for
short fits the start-up must pay for itself.  Both sets of derivatives are
the fit's own, so the trial computes nothing twice.  The trial is skipped
when the single-process timing already shows that no division of the work
could be 10% quicker, and the subprocesses are started only when they are
first given derivatives, so a fit that uses only analytic derivatives, or
stays in the main process, starts none.  Inside a subprocess of
`parallel total` (below), the decision carries from one fit to the
next while the models and noticed channels are the same.
The gain is therefore largest when the finite-difference derivatives are
many and expensive compared with one calculation of the whole model.  When a
single derivative dominates, nothing is gained, and the automatic choice
keeps to the main process.  An example is a
`phabs`*(`powerlaw` + 3 `gaussian`) fit to a
30000-channel spectrum, where every `phabs` calculation is costly
and only $n_H$ needs one: with `LEVEN_PARALLEL forced` the fit takes slightly longer with
`leven 4` than with `leven 1`.  Use `xset` `PARALLEL_TIMING`
(below) to see whether it helps with your model.

The `error` option is for running parallel computations within XSPEC's `error` command.
The searches for each parameter's lower and upper bounds run as separate
tasks, so the error calculation for $k$ parameters can keep up to $2k$
processes busy (a single parameter uses two).  The results are the same as
in single-process mode, whatever the number of processes.  If any search
finds a new minimum the other processes are stopped at once, the fit is
redone from the new minimum and the calculation restarts, as it does in
single-process mode.

When the `steppar` option is set, XSPEC cuts the grid into about
$\sqrt{n}$ pieces for $n$ grid points (between 4 and 64): whole rows of the
first stepped parameter when there are enough rows, otherwise segments of
rows.  The main process first fits the first point of each piece in turn,
each starting from the last, and the pieces are then handed to the
subprocesses as they become free, each starting from its first point's fit
and continuing point to point along its row.  The grid depends on the
number of points alone, so it is the same for any number of subprocesses;
it can differ slightly from a single-process grid, in which every point
continues from the one before.  The grid is printed when it is complete.

`parallel total` sets one budget of
processes shared by all the tasks.  With the default, `off`, each
task uses up to its own number, and while `error`, `steppar`,
`goodness`, `sim`, `coverage` or `lrt` runs in
parallel, the fits inside it run in a single process: the `leven`
setting is set aside until the command finishes.  With a total `<N>`,
each task's number becomes a ceiling, and every pool of subprocesses also
fits within the total.  A parallel `error`, `steppar`,
`goodness`,  run with $k$ subprocesses gives each of them
$N/k$ (rounded down), and the fits inside a subprocess can use a
`leven` pool within that share.  The process running a `leven`
fit calculates derivatives itself, so it counts as one of its share: a share
of 4 allows at most 3 `leven` subprocesses, and a fit outside any
other task with a total of 8 at most 7.  A subprocess keeps its
`leven` subprocesses from one fit to the next while it works on the
same piece of its task, as long as the free parameters, the models and the
noticed channels are unchanged, and stops them when the piece is done.  The
results are the same as with `off`.  `auto` sets the total to
the number of physical cores XSPEC may use (on Linux, those it is allowed to
run on, as in a batch allocation).  With a total, `xset`
`APECMULTITHREAD` also runs at most the process's share of threads:
one inside a subprocess or beside `leven` subprocesses.

Leave the outer task's own number at the total, or higher.  The outer pool
then takes as many subprocesses as it has tasks, and only the processes it
cannot use go to `leven` inside it: an `error` on one parameter
(two bound searches) on 64 cores, with `parallel total` 64,
`parallel error` 64 and `parallel leven` 64, gives each
search 32 processes, itself and 31 `leven` subprocesses.  Lowering
the outer number to make room for `leven` trades the outer division
of the work, which scales well, for the inner one, which gains only when the
fits' derivatives are many and expensive: on an 8-core test with a total of
8, `error` on three parameters took 15.8\,s with
`parallel error` 2 against 9.5\,s with 6.  When the total does not divide evenly, the first subprocesses get
one more.

On Linux, the subprocesses of an outer task still run their fits in a single
process under a total, until the combination has been tested there; setting
the environment variable `XSPEC_PARALLEL_NESTING=1` before starting
XSPEC enables it.

The `goodness` option is for parallelizing the calculations of the
simulated spectra during a `goodness` command run.  Each realization
draws its random numbers from its own stream, derived from the
`xset` `seed`, so the results are identical whether the run is
serial or parallel, and for any number of subprocesses.  The realizations
are handed out in small batches as subprocesses become free, as are those of
`sim`, `coverage` and `lrt`.

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
drawn in the parent process before the work is dispatched, and each
realization's counting noise comes from its own stream, so the results are
identical (and reproducible under `xset seed`) whether the run is
serial or parallel, and for any number of subprocesses.

The `tempering` option evaluates the rungs of
a tempered Metropolis-Hastings chain (`chain tempering`) in up to
`<N>` subprocesses, all the rungs' proposals of one step together. Each
rung draws from its own random stream, so the chain file is the same, row
for row, whatever `<N>` is. Set it to about the number of rungs.

The `coverage` option spreads the simulations
of the `coverage` command over up to `<N>` subprocesses.  Every
simulation draws from its own random stream, so the report is the same
whatever `<N>` is; inside a simulation the other tasks run in a single
process.

The `lrt` option does the same for the
simulations of `lrt` and `simftest`.

On a machine with many cores, a Monte Carlo Markov chain run with
`chain` `walkers` and `parallel walkers` `<N>`
is often the quickest way to parameter uncertainties for a slow model: the
statistic for all the walkers of a step is calculated at once, so the chain
can keep as many processes busy as it has walkers, where `error` uses
at most one per parameter.

To see how well a task is using its subprocesses, set
`xset` `PARALLEL_TIMING yes`.  Each pool of subprocesses then
prints a report when it closes: the task (for `leven`, which of its
three pools: folded-model columns, statistic gradient or statistic
curvature); the number of subprocesses; how many times work was handed out
(runs: for `leven` one per derivative calculation) and the number of
individual calculations (tasks); the time those runs took and how long the
pool was open; the fraction of the run time each subprocess spent
calculating (minimum, median and maximum); the tail ratio, the slowest
subprocess's calculating time over the average, summed over the runs (1 is
perfectly shared work); and the time the subprocesses spent receiving work and
returning results.  For the folded-model pool of `leven` it adds how
many derivative columns were analytic, calculated in the main process (and
how long the main process took over them), and how many were finite
differences, and when the main process computed some of the
finite-difference derivatives itself, how many and how long they took, and
how often the finite differences were started before the analytic
derivatives (and how often on a wrong guess of which derivatives are finite
differences, which only costs time), and with the automatic choice the
trials (the two timings) and how many derivative sets were then calculated
serially and how many in parallel.  A serial run reports nothing.  `PARALLEL_TIMING`
`<file>` appends the same numbers to `<file>` as one line of JSON
per pool instead, and `yes,``<file>` does both.
`tclout` `parallel timing` returns the last pool's numbers.

**Examples:**

```
XSPEC> model cflow
// Using a model with 5 variable fit parameters.

XSPEC> parallel leven 4
XSPEC> fit
// Calculations for the 5 parameters will be divided amongst
//	4 processes during the fit.

XSPEC> parallel leven 1
	// Restores single-process calculation to the
	//	Levenberg-Marquardt algorithm.

XSPEC> parallel error 3
	// Allow up to 3 simultaneous 'error' parameter calculations
	//	to be performed in parallel.

XSPEC> error 2 3 6
	// Perform error calculations on parameters 2, 3, and 6 in parallel.

XSPEC> parallel steppar 4
      // The following 20x30 grid is cut into 30 rows, handed out
      // to 4 parallel processes as they become free.
XSPEC> steppar 1 10. 11. 20 2 .5 .8 30

XSPEC> parallel total 8
XSPEC> parallel leven 8
XSPEC> parallel error 8
XSPEC> error 3
      // The two bound searches each get 4 of the 8 processes: the
      // search itself and up to 3 leven subprocesses.

XSPEC> xset PARALLEL_TIMING yes
XSPEC> parallel leven 4
XSPEC> fit
      // After the fit, one report per pool of subprocesses, e.g.
      // Parallel timing: leven (folded-model columns)
      //    4 workers, 5 runs, 60 tasks; 4.314 s in runs, pool open 5.109 s
      //    worker busy fraction: min 0.34, median 0.34, max 0.45; tail ratio 1.23
      //    worker transfer time: 5.231 s
      //    analytic columns 0, finite-difference columns 60

	// Display current settings:
XSPEC> parallel
Maximum number of parallel processes:
   coverage: 1
   error: 3
   global: 1
   goodness: 1
   hmc: 1
   leven: 1
   lrt: 1
   nest: 1
   sim: 1
   steppar: 4
   tempering: 1
   walkers: 1
   total: off
```
