---
name: chain
aliases: [xchain]
also_documents: [chainadapt, chainbest, chainburn, chainclear, chaindiag, chainfiletype, chaininfo, chainlength, chainload, chainproposal, chainrand, chainrecalc, chainrescale, chainrun, chainset, chainstat, chaintempering, chaintemperature, chaintype, chainunload, chainwalkers]
source: XSchain.tex
---

# chain

**run a Monte Carlo Markov Chain**

**Syntax:** `chain` [adapt on| off [target <rate>]] [best] [burn <length>] [clear] [diag]
[dic] [filetype fits| ascii] [info]
[length <length>] [load <filename>] [proposal [<distr>  <source>]
| [<user-defined>]] [rand on| off] [recalc] [rescale <factor>]
[run [>]<filename>]
[set median| mean| best]
[stat <par num>] [temperature <value>]
[tempering <K>| off [tmax <T>] [swap <n>] [adapt on| off] [sidefiles on| off]]
[type mh| gw]
[unload <range>] [walkers <value>]

If the proposal source is set to use the fit correlation matrix (the default), 
you must perform a fit before running any chains.

When chains are loaded (and their parameters correspond to the currently 
loaded model), they will be used by the various XSPEC commands that require 
distributions of parameter values, such as `eqwidth` or `flux`
when calculating error estimations.  The `error` command itself will 
also use the loaded chains, determining the error range from a central 
percentage of the sorted chain values.  This is likely to be faster than 
the `error` command's standard algorithm when not using chains.

- [`adapt on| off [target `<rate>`]`]Whether new Metropolis-Hastings chains adapt their proposal during the
burn-in (default `off`). While adapting, the proposal covariance is
re-estimated from the burn-in samples (adaptive Metropolis: $2.38^2/d$ times
their covariance, after the first $\max(100, 10d)$ steps; before that the
`proposal` setting's own matrix), and its overall scale is tuned so
that the acceptance rate approaches `<rate>` (default 0.234, the
optimum for a multi-dimensional random walk; 0.44 is the one-parameter
optimum). At the end of the burn-in the proposal is frozen: every recorded
step uses that one fixed proposal, so the chain is ordinary
Metropolis-Hastings and its diagnostics apply as usual. The run reports the
acceptance reached late in the burn-in and the final scale, and a FITS chain
file records them as the keywords `ADAPTTGT`, `ADAPTACC`,
`ADAPTSCL` and `ADAPTNB` (an ASCII chain file, whose header has
a fixed layout, does not). The frozen proposal then becomes the current chain
proposal, as if set with `proposal` or `rescale`, so an
appended run (`run` `>``<filename>`) continues with it.
This removes the trial and error of tuning a proposal by hand with
`rescale`, and it can also correct a proposal with the wrong
correlations (from a fit near a limit, or one built from the
`deltas`). Adapting needs a burn-in (`burn`) and a built-in
proposal (gaussian, cauchy or uniform with a covariance source); a run with
`burn 0`, a user-defined proposal or the `limits` source is
refused. Parameters that have not moved during the burn-in, such as one
pinned at a hard limit, keep the starting proposal's variance. The setting
has no effect on Goodman-Weare chains. `<rate>` must lie between 0 and 1.

- [`best`]Finds the parameter and
statistic values for the point in the loaded chains with the best statistic value.

- [`burn` `<length>`]Specifies that the first `<length>` steps should be thrown away prior to storing the chain.

- [`clear`]Does a reset and removes all
chains from the list.

- [`diag`]Prints the Markov-chain
  convergence and effective-sample-size diagnostics of
  Vehtari et al. (2021) for the loaded chains.  For each variable
  parameter the report tabulates the classical split Rhat, the
  rank-normalized Rhat, the bulk and tail effective sample sizes (ESS),
  the integrated autocorrelation time $\tau$ and the ratio $N/\tau$,
  and, for Goodman-Weare chains, the per-walker sticky-walker ratio
  ($\tau_{\rm max}$/median), together with a 1-D marginal bimodality
  coefficient.  The report opens with a one-line verdict:

- `[ OK ]` if every check is within its threshold;
    
- `[WARN]` if one or more checks fail (each failing check
      is then listed);
    
- `[SHORT]` if the chain is too short (fewer than 8
      samples per sub-chain) for the diagnostics to be defined.
  
  The warning thresholds are fixed: rank-normalized Rhat $< 1.01$;
  bulk-ESS and tail-ESS $\geq 400$; $N \geq 50\,\tau$; and, for
  Goodman-Weare, a walker $\tau$ ratio $< 10$.  The bimodality coefficient
  is advisory only --- a value above $5/9$ suggests a flat-topped or
  multi-modal marginal and points you at `nest` for rigorous mode
  separation --- and does not by itself raise a `[WARN]`.  The full
  report is also printed automatically at the end of a successful
  `chain run`, and the one-line verdict is appended to the output
  of `chain info`.

- [`dic`] Calculates the Deviance Information Criterion and
the effective number of parameters for the loaded chains.

- [`filetype fits| ascii`]Chooses the format of the output chain file. `fits` (the
  default) writes the chain to a binary table in a FITS
  file. `ascii` writes the chain to a simple text file.  Either
  format is readable when using the `chain load` command.

- [`info`]Prints out information on the
  current chains, followed by the one-line convergence verdict described
  under `chain diag`.

- [`length` `<length>`]Sets the length for new chains.

- [`load` `<filename>`]Loads a chain
  which has been run earlier, stored in file given by `<filename>`.

- [`proposal` `<distr>`  `<source>`]Selects the proposal distribution and source of covariance
  information to be used when running new chains. For the
  Metropolis-Hastings algorithm this distribution is used at each step
  of the chain while for the Goodman-Weare algorithm it is only used
  to set the initial walkers. The default is
  `proposal gaussian fit`. Currently implemented `<distr>`
  options are: `gaussian`, `cauchy`, and `uniform`. `<source>`
  options are:

- [`chain`] Covariance is taken from the currently loaded chains.
  
- [`deltas` `<value>`] A diagonal covariance matrix
    is constructed from the parameter deltas multiplied by the value
    entered on the command line.
  
- [`diagonal` `<values>`] The values of a diagonal covariance matrix 
    are entered directly on the command line, separated by commas and/or spaces: 
    `C_11 C_22 ... C_nn`.
  
- [`<filename>`] Covariance is read in from a user-specified text file.  
    The file must contain the values of an NxN matrix where N is the current 
    number of freely varying parameters.  The values of each matrix row should 
    be entered on one line with whitespace separation.  
    Since this matrix is always symmetrical, values above the 
    diagonal may be omitted.  For example a 2x2 matrix  could be entered as:
    
```
        0.98
        0.15 0.96
    
```

- [`fit`] Covariance is taken from the correlation
    information produced by the current fit.
  
- [`limits`] Used only for the `uniform` option and
    draws uniformly from the entire parameter space defined by the
    parameter hard limits.
  
- [`matrix` `<values>`] The lower half and diagonal
    of a symmetrical square covariance matrix are entered directly on
    the command line, separated by commas and/or spaces:
    `C_11 C_21 C_22 C_31 C_32 C_33 ... C_nn`
  
  The `uniform` `<distr>` option only accepts
  `<source>` values of `deltas` or `limits`.
  `chain proposal` with no other arguments will show a list of
  all available proposal options. For an alternative to XSPEC's
  `<distr>` `<source>` proposal options, the user may
  instead want to provide their own custom randomization algorithm.
  This can be done by writing their own C++ class(es) derived from an
  XSPEC randomizer base class.  The custom class is added at runtime
  using the same `initpackage` or `lmod` command sequence
  as for local models, and is specified by `proposal`
  `<name>` where `<name>` is the unique name attribute the
  user provides for their class. Please see
  Appendix AppendixChainProposal 
  for more information on writing a custom randomizing class, and
  `initpackage` for building and loading it.

- [`rand on| off`]Specifies whether the chain start point will be randomized, or taken from the current parameters.

- [`recalc`]A deprecated option that performs the equivalent of `proposal gaussian chain`.

- [`rescale `<factor>``] Rescale
  the covariance matrix used in the proposal distribution by the factor given.

- [`run [>]` `<filename>`]Runs a new chain written to the specified file, or append to an
  already loaded file if the '>' character preceeds the
  filename.  The chain is written to the file as it runs so its
  performance can be monitored by examining the file.  For
  high-chatter settings, additional information is printed to the
  screen. A long run may be interrupted with Ctrl-C, in which case the
  chain file will still exist but will not be automatically loaded.
  If appending to a file, the current `filetype` setting must
  match the format of the file or XSPEC will prevent it.  On successful
  completion the convergence diagnostics (see `chain diag`) are
  printed.

- [`set median| mean| best`]Moves every variable parameter onto one point of the loaded chains:
  the median of each parameter, its mean, or the point with the lowest
  fit statistic (the one `chain best` reports).  For an
  importance-weighted chain, such as the output of `nest`, the
  median and mean are the weighted ones; the median is then the point
  at which the cumulative weight reaches one half, read off the same
  weighted distribution `error` takes its interval from.  The best
  point does not depend on the weights.

  The estimator must be given; there is no default.  The three can
  disagree badly on a posterior with more than one mode, and choosing
  between them is a judgement about the problem rather than a setting.

  Before moving the parameters the command checks the posterior for more
  than one mode: a bimodality coefficient above $5/9$ on any parameter
  (the same test `chain diag` applies), or a `nest` run
  of the loaded file that found several modes.  Either prints a warning
  naming the cause, and the parameters are *still* moved --- a
  median taken across two modes may sit in neither of them, and the
  warning says so, but it is not grounds for refusing.

  Only parameter values change.  Error bounds are left as they were; use
  `error` to compute the chain's interval.  The loaded chains must
  match the current variable parameters, as they must for `error`
  to read them.  The fit statistic at the new values is printed, as it
  is after `newpar`, followed by each parameter's previous and new
  value.

- [`stat [<modName>:]<parIdx>`]Writes out statistical information on a particular parameter of the
  chain, specified by the parameter index number. If the parameter is
  from a named model then it is indicated by
  `[<model name>:]<n>`. If the parameter is from a
  response model then use the format
  `[<source number>:]r<n>`. If the parameter number is
  zero then the information is about the fit statistic.  The information displayed
  is:

- The mean of the parameter in each chain.
    
- If there are multiple chains, the parameter mean over all 
      chains and the variance between chain means.
    
- The variance over all the chains.
    
- If there are multiple chains the Rubin-Gelman convergence
      measure.
    
- The Geweke convergence measure.
    
- If using Metropolis-Hastings, the fraction of repeats,
      defined as the number of lines in the chain
      file for which all parameter values are identical to the previous
      line, divided by the number of lines in the file.
    
- The modern diagnostics of Vehtari et al. (2021) for
      this parameter (rank-normalized Rhat, bulk- and tail-ESS, integrated
      autocorrelation time, the bimodality coefficient, and, for
      Goodman-Weare, the walker $\tau$ ratio); see `chain diag`.

- [`tempering` `<K>`|`off` [`tmax` `<T>`] [`swap` `<n>`] [`adapt on| off`] [`sidefiles on| off`]]Parallel tempering for new Metropolis-Hastings chains (default
  `off`). `<K>` ($\geq 2$) chains, or rungs, run together at
  temperatures $T_1 = 1 < T_2 < \dots < T_K = $`<T>` (default 100),
  spaced geometrically; rung $k$ samples the posterior raised to the power
  $1/T_k$, so the hotter rungs see a flatter surface and cross between
  modes that would trap a single chain. Every `<n>` steps (default 10)
  each pair of adjacent rungs, hottest first, proposes to exchange states,
  accepted with probability
  $\min\{1, \exp[(1/T_k - 1/T_{k+1})(S_k - S_{k+1})/2]\}$ for fit statistics
  $S$. Only the $T = 1$ rung samples the posterior, and only it is written
  to the chain file; all the usual diagnostics apply to it unchanged. As a
  guide, $K$ of about $\sqrt{d}$ to a few times that, for $d$ free
  parameters, with `<T>` large enough that the hottest rung moves freely
  between the modes.

  Each rung draws its step from the current `proposal`, scaled by
  $\sqrt{T_k}$. With `adapt on` (or, by default, whenever
  `chain adapt` is on) the temperatures are tuned during the burn-in
  so that the swap acceptance is the same for every adjacent pair
  (Vousden, Farr & Mandel 2016, with $T_K$ held at `<T>`);
  under `chain adapt` each rung also tunes its own proposal scale
  towards the adapt target. The proposal's covariance is not re-estimated
  while tempering: after swaps the $T = 1$ samples mix modes and their
  covariance is the wrong shape for local steps. Both are frozen at the end
  of the burn-in, so the recorded chain comes from one fixed scheme. The run
  reports the temperatures, the rung proposal scales, the burn-in acceptance
  of each rung and the swap acceptance; a FITS chain file records the
  ladder as `PTRUNGS`, `PTSWAP`, `PTADAPT` and, per
  rung, `PTT`$k$, `PTSCL`$k$ and `PTACC`$k$ (the swap
  acceptance of rungs $k$ and $k+1$ over the recorded steps), which
  `chain info` and `tclout` `chain tempering| swap` read
  back. `sidefiles on` writes rungs 2 to $K$ to
  `<stem>``_T`$k$`<ext>` beside the chain file, for
  diagnostics; they are never loaded automatically, and loading one by hand
  gives a chain at temperature $T_k$.

  The rungs of each step are evaluated together, spread over
  `parallel tempering` processes. Every rung draws from its own
  random stream derived from the session seed, so the chain file is the
  same whatever the number of processes. Refused: `type gw`, a
  `temperature` other than 1 (the bottom rung is $T = 1$), a
  user-defined proposal or the `limits` source, ladder adaptation
  with `burn 0`, and appending either to a tempered chain (the
  hotter rungs' states are not in the file) or while tempering is on.
  Options left off the command line take their defaults, so the command
  always states the whole setting.

- [`temperature` `<value>`]Sets the temperature parameter used in the Metropolis-Hastings
  algorithm for the proposal acceptance or rejection.  The default
  value is 1.0 and zero or negative values are forbidden.  By using
  the run append option, it is possible for different sections of the
  chain file to use different temperatures.  The temperatures and the
  line numbers to which they apply are stored in the header of the
  FITS format chain files, or in the metadata section at the top of
  the ASCII text format files.

- [`type mh| gw`]Determines the
  algorithm used to generate the chain.  Choices are `mh`
  (Metropolis-Hastings) or `gw` (Goodman-Weare, the default).
  If using Goodman-Weare, must also set the `walkers`
  parameter.  Also note for Goodman-Weare that the calculation of 
  `walkers` sets may be sped up by adjusting the `parallel`
  command's `walkers` option to perform the calculations over
  multiple processes. The walkers are initialized in two different
  ways depending on whether a fit has previously been run. If a fit
  has been run and a covariance matrix is available then walkers are
  initialized by drawing from a multi-Normal distribution whose
  variance matrix is based on the covariance matrix. If a covariance
  matrix is not available then parameters in each walker are
  initialized by drawing from a uniform distribution centered on the
  current fit parameters with width ten times that of the parameter
  delta. Initial values for walkers can also be generated outside
  xspec and then imported by writing them to a standard FITS chain
  output file with number of rows equal to number of walkers. If a
  chain is now run using the append option ($>$ before the filename)
  then the starting values for each walker will be taken from the file.

- [`unload` `<range>`]Removes the
  chains specified by `<range>` from the list in xspec.  Note
  that this does NOT delete the chain files.

- [`walkers` `<value>`]Sets the
  `walkers` parameter for the Goodman-Weare chain algorithm
  (see `chain type`). This must be an even integer, and both the
  chain length and burn length should be divisible by it (XSPEC will
  adjust the lengths to make them so if necessary).

All loaded chains must contain the same fit parameters.  xspec will prevent 
the loading of a chain with a different number of parameters from the 
currently loaded chains.

**Algorithm notes**

For the Goodman-Weare (gw) choice the method used to derive new
parameter values for the walkers is as follows.

- Divide the walkers into two sets (to allow parallelization)

- For each walker, W, randomly choose a walker, U, from
  the other set

- Draw a random number Z from the distribution 1/$\sqrt(z)$, where
  z lies between 0.5 and 2.0.

- Set the new parameters for W to Z*parameters(W) + (1-Z)*parameters(U)

- Calculate a new fit statistic with these parameters then
  calculate T = (N-1)*log(Z) - 0.5*(newStat-oldStat) where N is the number
  of fit parameters

- Draw a random number from a uniform distribution between 0 and 1
  and if the ln of this random number is less than T then accept the
  new parameter values otherwise repeat the old parameter values.

**Examples:**

```
XSPEC>chain length 100 
//Sets length of chains produced by the run command to 100.
XSPEC>chain run chain_file1.out
//Runs a chain based on current valid fit parameters, output to 
//chain_file1.out
XSPEC>chain run >chain_file1.out
//Appends another run of length 100 to the end of chain_file1.out
XSPEC>chain load chain_old.out
//Loads a pre-existing chain file, the result of an earlier run 
//command.  Warning is issued if not the same length as 
//chain_file1.out
XSPEC>chain stat 3
//Prints statistical information on the 3rd parameter of the chain.
XSPEC>chain proposal gaussian myfile.txt
//New chain proposals will be a normal distribution using
//covariance values stored in myfile.txt rather than fit
//correlation matrix. 
XSPEC>chain prop gauss diag .1 .001 .0001
// New chain proposals will be a normal distribution using a 3x3
// diagonal covariance matrix with the values from the
// command line. 
XSPEC>chain tempering 6 tmax 100
// New Metropolis-Hastings chains run a 6-rung parallel-tempering
// ladder; only the T = 1 rung is written to the chain file.
XSPEC>parallel tempering 6
// ... with the rungs of each step evaluated in 6 processes.
XSPEC>chain temperature .8
// Sets the Metropolis-Hastings temperature value to .8 for
// future chain runs, replacing the default 1.0.
XSPEC>chain clear
//Removes the 2 loaded chains from xspec's chain list.
```
