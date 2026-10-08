---
name: tclout
aliases: [xtclout]
also_documents: [tcloutcleared, tcloutbias, tcloutcgof, tcloutchain, tcloutderror, tcloutdmodel, tcloutdpar, tclouteqwidth, tclouterror, tcloutflux, tcloutgain, tclouthmc, tcloutlumin, tcloutmixweights, tcloutnchan, tcloutnest, tcloutpeakrsid, tcloutplot, tcloutrmodel, tcloutrpar, tcloutsigma, tcloutsim, tcloutsteppar, tcloutversion]
source: XStclout.tex
---

# tclout

**create tcl variables from current state**

Write internal xspec data to a tcl variable. This facility allows the 
manipulation of xspec data by tcl scripts, so that one can, for example, 
extract data from xspec runs and store in output files, format xspec 
output data as desired, use independent plotting software, etc.

**Syntax:** `tclout` <option> [<par1>] [<par2>] [<par3>]

`tclout` creates the tcl variable `$xspec_tclout`, which can then of course be 
set to any named variable.

The results of the analysis commands describe the data
and models they were computed on.  Loading data (`data`, including
`data none` and removing spectra) and defining or changing a model
(`model`, `addcomp`, `delcomp`, `editmod`) clear
them, and the options below that read them -- `error`, `sigma`,
`goodness`, `ftest`, `sim`, `nest`,
`hmc`, `steppar`, `margin`, `flux`,
`lumin`, `eqwidth`, `lrt`, `coverage`,
`cgof` and `bias` -- then return what they return before the
command has been run.  `fit`, `newpar`, `ignore`,
`notice`, `response` and `backgrnd` do not clear them, so
`fit`, `error 1`, `tclout error 1` works, and so does
reading a result after adjusting something to look at it.  Loaded chains are
not affected.

The allowed values of `<option>` are:

 |p{0.61}} 
`?` & Show the valid options. Does not set $xspec_tclout.

`areascal n` `<s| b>` & Writes a string of blank separated values giving the AREASCAL values for spectrum n.  
If no second argument is given or it is ``s'' then the values are from the source file, if ``b'' from the background file.

`arf n` & The auxiliary response filename(s) for spectrum n.

`backgrnd n` & Background filename for spectrum n.

`backscal n` `<s| b>` & Same as areascal option but for BACKSCAL value.

`bayes` & The current Bayesian prior settings, in the same form
printed by the `bayes` command (including any joint priors).

`bias [bias| percent| first| debiased|
  pars| verdict]`& Results of the last `bias`
command, one value per free parameter in fit order: `bias` (the default)
the predicted bias in parameter units, `percent` the same as a
percentage of the debiased value, `first` the first-order estimate,
`debiased` the debiased value $\theta_0$, `pars` the parameter
numbers (`model:n` for a named model).  When the last run ended in the
collapse verdict the numeric reads (other than `first`) are empty and
`verdict` returns the verdict sentence; otherwise `verdict` is
empty, so a script tests it first.  An error if no `bias` has run
since the last refused one.

`cgof [expected| sd| zscore| pvalue| fhat|
  sys| delta]`& Results of the last `cgof`
command.  With no option, four values: $E[C]$, its standard deviation,
$(C-E[C])/{\rm sd}$ and the one-sided $p$-value without systematics;
`expected` the first two of these, `sd`, `zscore` and
`pvalue` each one of them; `fhat` the implied relative
systematic $\hat f$ with its 68% lower and upper bounds; `sys`
the run with systematics, $f$, $\mu_C$, $\sigma_C$, $E[C_{\rm sys}]$, its
sd, $(C-E)/{\rm sd}$ and $p$ (empty unless `f` was given);
`delta` the last `cgof` `delta`: $\Delta C$, $k$, $f$,
$\mu$, $\alpha$, the nominal $p$ and the $p$ with systematics.  An error if
no `cgof` (or `cgof` `delta`) has run since the last
refused one.

`chain best| dic| last| proposal|
  stat`& The best option returns 
the parameter values corresponding to the smallest statistic value in the 
loaded chains. The dic option returns the deviance information
criterion and effective number of parameters calculated by the last
chain dic command. The last option returns the final set of parameter values in 
the loaded chains. The proposal option takes arguments distribution or matrix 
and returns the name or covariance matrix for the proposal distribution when 
using Metropolis-Hastings. The stat option returns the output of the 
last chain stat command.

`chatter` & Current xspec chatter level.

`compinfo [<mod>:]n [<group n>]` & Name, 1st parameter number and number 
of parameters of model component n, belonging to model w/ optional name <mod>
and optional datagroup <group n>.

`cosmo` & Writes a blank separated string containing the Hubble constant (H0), 
the deceleration parameter (q0), and the cosmological constant (Lambda0).  
Note that if Lambda0 is non-zero the Universe is assumed to be flat and 
the value of q0 should be ignored.

`covariance [m,n]` & Element (m,n) from the covariance matrix of the most recent fit.  
If no indices are specified, then entire covariance matrix is retrieved.

`datagrp [n]` & Data group number for spectrum n.  If no n is given, outputs the 
total number of data groups.

`datascan [drift| flagged| pars| setups|
cond| corr| stat]` & From the last `datascan`: per row
of its drift table, the largest $|\Delta|/\sigma$ (the default; $-1$ where
none could be computed), whether it is flagged (1/0), the parameter, or the
setup; or per setup, the session's first, its largest `projct`
condition number ($-1$ without `projct`), its most negative
adjacent-shell correlation ($1$ without `projct`) or its fit
statistic.

`datasets` & Number of datasets.

`derror n`& The last confidence region calculated for data
parameter n (see `dmodel`), and the error string, as for `error`.

`dmodel <specNum>`& The names of the data models
attached to spectrum <specNum>, in order of application; empty if none.

`dof` & Degrees of freedom in fit, and the number of channels.

`dpar n`& Value, delta, min, low, high, max of data
parameter n, as `param` does for a model parameter.

`energies [n]` & Writes a string of blank separated values giving the 
energies for spectrum n on which the model is calculated.  If n is not 
specified or is 0, it will output the energies of the default dummy 
response matrix.

`eqwidth n [errsims]`& Last equivalent width calculated for spectrum n.  
If `errsims` keyword is supplied, this will instead return the 
complete sorted array of values generated for the most recent eqwidth error 
simulation.

`error [<mod>:]n`(for response parameters use: `rerror [<sourceNum>:]n`) &
Writes last confidence region calculated for parameter n of model with optional 
name <mod>, and a string listing any errors that occurred during the 
calculation.  The string comprises nine letters, the letter is T or F 
depending on whether or not an error occurred.  The 9 possible errors are:

- new minimum found

- non-monotonicity detected

- minimization may have run into problem

- hit hard lower limit

- hit hard upper limit

- parameter was frozen

- search failed in -ve direction

- search failed in +ve direction

- reduced chi-squared too high

So for example an error string of ``FFFFFFFFT'' indicates the calculation 
failed because the reduced chi-squared was too high.

`expos n` `<s| b>` & Same as areascal option but for EXPOSURE value.

`filename n` & Filename corresponding to spectrum n. If the
filename is type II then include the {n} suffix specifying the row
from which the spectrum was read.

`fileinfo` `<keyword>` `n` & Value of keyword in the SPECTRUM
extension of the file corresponding to spectrum n.

`flux [n][errsims]`& Last model flux or luminosity calculated for spectrum n.  
Writes a string of 6 values: val errLow errHigh (in ergs/cm2) val errLow 
errHigh (in photons).  Error values are .0 if flux was not run with `errsims` option.

If the `errsims` keyword is supplied, this will instead return the 
completed sorted array of values generated during the most recent flux error calculation.

`ftest` & The result of the last ftest command.

`gain [<sourceNum>:]<specNum> slope|
  offset`&
Value, delta, min, low, high, max for the slope or offset parameter of the
`gain` model attached to the [<sourceNum>:]<specNum> response
(six fields whether or not the parameters are frozen).  With no gain
attached, the nominal value alone (1 or 0).

`coverage [fraction| sigma| below| above|
flagged| failed| pars| nominal]` & From the last
`coverage` command, one value per tested parameter: the fraction of
intervals containing the truth (the default), its binomial $1\sigma$, the
fractions lying wholly below and above the truth, the flagged and failed
counts, or the parameter identifiers.  `nominal` gives the nominal
rate and the $\Delta$-statistic used.

`lrt [p| observed| stat| sims]` & From the last
`lrt` or `simftest`: the p-value and its binomial error (the
default), the observed statistic difference (null minus alternative), the
null's and the alternative's statistics, or every simulation's difference.

`goodness [sims]` & The percentage of realizations from the last goodness
command with statistic value less than the best-fit statistic using the data.
If optional `sims` keyword is specified, this will instead give the
full array of simulation values from the last goodness command.

`group <n> [data| back] [intent]` & The grouping information
for spectrum n.  With `data` (the default) this returns the per-channel
grouping flags (1 starts a new bin, $-1$ continues it, 0 marks a bad channel);
with `back` it returns the per-channel super-bin (pooling) index of the
background.  If the `intent` keyword is added, the grouping intent is
returned instead (`original`, or one of `minsn`,
`mincounts`, `const`, `optbin` with its value,
`auto` with its count target and resolution cap, or
`file` with the filename).

`hmc [divergent| accepted| meanaccept|
  samples| grads| verdict| pars| par n]`%
& Results of the last `hmc` run.
`divergent` (the default), `accepted`, `meanaccept`,
`samples` and `grads` are the numbers its finish line quotes.
`verdict`, `pars` and `par` `n` behave as for
`nest`; the verdict is the ordinary chain diagnostic plus the
divergence count.  An error if no `hmc` has run.

`idline e d` & Possible line IDs within the range [e-d, e+d]. 

`ignore [<n>]` & The range(s) of the ignored channels for spectrum n.

`lumin [n] [errsims]`& Last model luminosity calculated for spectrum n.
Same output format as flux option, in units of $1.0\times 10^{44} erg/s$.

`margin probability | fraction | integprob |\
  [<modName>:]<parNum>` &
The probability and fraction options return the probability and
fraction columns, respectively, from the 
most recent margin command.  The integprob option returns the integrated 
(cumulative) probability column that `plot integprob` contours --- see 
`margin` for how it is accumulated and what it is normalized over.  
Otherwise, the parameter column indicated by 
<parNum> is returned.  Note that for multi-dimensional margin the returned 
parameter column will contain duplicate values, in the same order as they 
originally appeared on the screen during the margin run.

`mixweights [<modName>:]<n> [<energy>]`& The weights
with which mixing model component <n> mixes the spectra, at its current
parameter values: one list per mixing set (`projct` and the PSF and
cluster-mass models have one per observation, other models one), holding the
set's spectrum numbers and then one row per target spectrum, the weight with
which each source spectrum's model reaches it (0 for a pair the model does
not mix).  For example `{{1 2} {0.9 0.1} {0.1 0.9}}`.  Weights
that depend on energy are given at <energy> (keV), which they then
require: the factor the mix applies in the target's model energy bin
containing it (NaN outside the target's model energies).  An error for a
component that is not a mixing model, and for one with no weights to give:
old-style local mixing models mix in their own code.

`model` & Description of current model(s).

`modcomp [<modName>]` & Number of components in model (with optional model name).

`modgroups [<modName>]` & The data group numbers associated with a 
model  (with optional model name).

`modinfo <component>` & The definition of a model component,
loaded or not (as `model ? <component>` shows it): name, type,
origin (`built-in`, `local`, `python` or
`mdefine`), the local package or the `mdefine` expression (else
empty), minimum and maximum energy, gradient (`none`, `g` or
`gv`), spectrum dependence (0/1), and the list of keyed model
description tokens; then one list per parameter: name, unit, kind
(`param`, `switch` or `scale`), default, hard minimum,
soft minimum, soft maximum, hard maximum and delta (a switch or scale
parameter repeats its default in the four limits and has delta 0).

`modnames` & The names of models. 

`modkeyval [<key>]` & The value attached to <key> in
the model (key,value) database. Key and value pairs can be added to
this database by calling in a function routine the method
loadDbValue(const string key, Real value) for C++ or
PDBVAL(character*(*) key, double precision value) for Fortran. A list
of the current (key,value) pairs can be obtained by entering ``?'' for
<key>.

`modpar [<modName>]` & Number of model parameters(with optional model name).

`modval [<specNum> [<modName>]]` & Write to Tcl the last calculated model 
values for the specified spectrum and optional model name.  Writes a string of 
blank separated numbers.  Note that the output is in units of 
$photons/cm^2/s/bin$.

`nchan [<n>]`& Total number of channels in spectrum n (including ignored channels).

`nest [logz| logzerr| h| modes| ess|
  calls| iters| nlive| termination| converged|
  verdict| pars| par n]`& Results of the
last `nest` run.  `logz` (the default) and `logzerr` the
evidence and its uncertainty, `h` the information $H$, `modes`
the final ellipsoid count, `calls` and `iters` the likelihood
evaluations and outer iterations, `nlive` the live points the run
finished with, `termination` the reason it stopped and
`converged` 1 when that reason was the $\Delta\log Z$ tolerance.
`ess` is the Kish effective sample size, read off the loaded weighted
chain rather than the run record, since it is a property of the weights.
`verdict` returns the status word (`OK` or `WARN`) on the
first line and one failing check per line after it, so a script can branch on
`lindex 0`.  `pars` lists the parameter numbers
(`model:n` for a named model) and `par` `n` the credible
interval for the $n$th of them --- the same interval `tclout`
`error` reports for that parameter, because it is the same
computation.  An error if no `nest` has run.

`noticed [<n>]` & Range (low,high) of noticed channels for spectrum n.

`noticed energy [<n>]` & The noticed energies for spectrum n.

`nullhyp` & When using chi-square for fits, this will retrieve the reported null 
hypothesis probability.

`parallel timing` & For the last pool of parallel subprocesses
(`xset` `PARALLEL_TIMING`, see `parallel`): task,
{pool}, subprocesses, runs, tasks, run time and time open (seconds), the
minimum, median and maximum busy fraction, the tail ratio, the transfer time
(seconds), and a list of {{name} value} totals.  An error before any
pool has run.  `par` and shorter still mean `param`.

`param [<mod>:]n` & (value, delta, min, low, high, max) for model parameter n.

`peakrsid n [lo,hi]`& Energies and strengths of the peak residuals (+ve and -ve) 
for the spectrum n. Optional arguments lo, hi specify an energy range in 
which to search.

`pfree [<mod>:]n` & T returned if parameter is free, F if not.

`pinfo [<mod>:]n` & Parameter name and unit for parameter n of model
with optional name.

`plink [<mod>:]n` & Information on parameter linking for parameter n. 
This is in the form true/false (T or F) for linked/not linked, followed 
by the multiplicative factor and additive constants if linked.

`plot <option> <array> [<plot group n>]` &
Write a string of blank separated values for the array.  <option>
is one of the valid arguments for the plot or iplot commands.  <array> 
is one of x, xerr, y, yerr, yerrlow, model, bandlow or bandhigh.  bandlow and
bandhigh are the edges of the first level of the credible band
(`setplot band`).  xerr and yerr output the 1-sigma error
bars generated for plots with errors; for a plot with asymmetric y errors
(`plot param`) yerr is the upper and yerrlow the lower bar, and for any
other plot yerrlow equals yerr.  A plot type that takes arguments is written
with them, before the array: `tclout plot param 1 groups y`.  The model array is for the convolved
model in data and ldata plots.  For contour plots this command just dumps the
steppar results.  Plot groups are numbered through the whole plot, so for
`plot corner`, which draws many panes, <plot group n> counts
across them: the panes run column by column, top down; a diagonal pane holds
four groups (the histogram, then the median and the lower and upper interval
as vertical lines) and a two-parameter pane one group per closed region
boundary, the 68.3% region's first.  A subset is given after a colon, as a
named model is: `tclout plot corner:1-3 y 1`.  On a log axis a
histogram's x array is each bin's arithmetic centre and xerr its
half-width, so x $\pm$ xerr are the bin's edges.

`plotgrp` & Number of plot groups.

`projct [cond| corr] [`<model name>`]` & For the
`projct` component of the (named) model, one value per observation:
the condition number of its shell-to-annulus matrix (the default), or the
strongest correlation between radially adjacent shells.  As of the last time
the matrix was built (the first evaluation after a model or data
change).

`query` & The setting of the query option.

`rate <n| all>` & Count rate, uncertainty, model rate, and 
percentage of net flux (no background) compared to total flux for the specified 
spectrum `n`, or for the sum over all spectra.

`rerror [<sourceNumber>:]n` & Writes last confidence region calculated for response 
parameter n of model with optional source number, and a string listing any 
errors that occurred during the calculation. See the help above on the 
error option for a description of the string.

`response n` & Response filname(s) for the spectrum n.

`rmodel [<sourceNum>:]<specNum>`& The names of the
response models attached to the [<sourceNum>:]<specNum> response, in
order of application (see `rmodel`); empty if none.

`rpar [<sourceNum>:]n`& Value, delta, min, low, high, max of
response parameter n of the source, as `param` does for a model parameter.

`sigma [<modelName>:]n`& The sigma uncertainty value for parameter n.
If n is not a variable parameter or fit was unable to calculate sigma, -1.0 is returned.

`sim <option>`& Results of the last `sim` command.
The `option` is one of: `n` (number of realizations); `stat`
(test statistic of each realization); `fitstat` (refit statistic of each
realization, fit runs only); `pars i`, `fitpars i` (drawn / refit
parameter values of realization i); or `result i` (the $xspec_simresult
list harvested from the sim command file for realization i).  The index i is
1-based.

`simpars` & Creates a list of parameter values by drawing from a multivariate
Normal distribution based on the covariance matrix from the last fit.  
This is the same mechanism that is used to get the errors on fluxes and 
luminosities, and to run the goodness command.

`solab` & Solar abundance table values.

`stat [test|<n>]` & Value of statistic.  If optional `test` argument is given,
this outputs the test statistic rather than the fit statistic.  If a spectrum number n is given, the fit statistic contribution from that one spectrum
is returned.

`statmethod [test]` & The name of the fit stat method currently in use.  
If optional `test` argument is given, this will give the name of the 
test stat method.

`steppar statistic |   delstat |   minima |
  [<modName>:]<parNum>`&
The `statistic` and `delstat` options return the statistic or
delta-statistic column respectively from the most recent steppar run.  The
`minima` option returns the grid-resolution local minima found by that
run: the first two numbers are the number of minima and the number of stepped
parameters, followed by one group per minimum (ordered best-first) giving the
delta-statistic and the parameter value(s) at that minimum.
Otherwise, the parameter column indicated by <parNum> is returned.
Note that for multi-dimensional steppars the returned parameter column will 
contain duplicate values, in the same order as they originally appeared on 
the screen during the steppar run.

`systematic [<modName>|unnamed]` & The current model systematic error values.
If no argument is given, this returns the default systematic value applied to
all models except those that have explicitly been assigned their own value.  If
a <modName> is given, this returns the systematic error value for that
specific model.  This will be the same as the default setting unless it has
been explicitly assigned its own value. To get the specific setting for an unnamed
model, enter `unnamed`.

`varpar` & Number of variable fit parameters.

`version`& The XSPEC version string.

`weight` & Name of the current weighting function.

`xflt n` & XFLT#### keywords for spectrum n. The first number written is the
number of keywords and the rest are the keyword values.

`xset <name>` & The value of any name `xset` accepts: a
named setting, abbreviated as `xset` allows (`abund`,
`cosmo`, `delta`, `mdatadir`, `method`,
`seed`, `statistic`, `usechainrule`, `weight`,
`xsect`); a control switch, its default when it has not been set (see
`xset`); or a model string from the `xset` string database.  An
error is reported if <name> is none of these.

**Examples:**

```
XSPEC>data file1
XSPEC> model pha(po)
...
XSPEC> fit
...
XSPEC>tclout stat
XSPEC>scan $xspec_tclout "%f" chistat
XSPEC>tclout param 1
XSPEC>scan $xspec_tclout "%f" par1
XSPEC>tclout param 2
XSPEC>scan $xspec_tclout "%f" par2
XSPEC>tclout param 3
XSPEC>scan $xspec_tclout "%f" par3
```

In this example, `scan` is a tcl command that does a formatted read of
the variable $xspec_tclout. It reads the first floating point number into
the variable given by the last argument on the line. This sequence creates a
simple model, fits it, and then writes the chi^2 statistic and the three
parameters to tcl variables $chistat, $par1, $par2, and $par3. These can 
now be manipulated in any way permitted by tcl. Examples of using tclout and 
tcloutr can be found in the Xspec/src/scripts directory.
