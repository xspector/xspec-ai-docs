---
name: xset
aliases: [xxset]
also_documents: [xsetdelta, xsetlist, xsetmdatadownload, xsetseed, xsetcontrolstrings]
source: XSxset.tex
---

# xset

**set variables for XSPEC models**

Modify a number of XSPEC internal switches.

**Syntax:** `xset` [abund | cosmo | delta | 
mdatadir | method | seed | statistic | usechainrule
| weight | xsect | <string_name> ]
[ <options> | <string_value> ]

With no arguments `xset` lists every setting, in
three blocks.  First the named settings -- the same lines
`show control` ends with: the fit statistic (or the default one, when
no spectrum is in the fit), the test statistic, the chi-squared weighting, the
fit method with its convergence criterion and proportional delta, the chain
rule, the abundance and cross-section tables, the cosmology, the model data
directory and the random-number seed.  Then every control switch in the table
below with its value, `(default)` marking one that is unset or set to
its default, and the values it accepts.  Last the model strings that have been
set.  `tclout xset` `<name>` returns the value of any name
`xset` accepts: a named setting (abbreviated as here, so
`tclout xset ab` is the abundance table), a control switch (its default
when it has not been set) or a model string.

The arguments `abund, cosmo, method, statistic, weight`, and `xsect` 
just run the appropriate XSPEC commands. `mdatadir` changes the 
directory in which XSPEC searches for model data files. You probably don't 
want to change this.

When a model needs a model data file that is not
in that directory, and the file is listed in XSPEC's catalog of model data
files (`modelDataFiles.csv` in the `spectral/manager`
directory), the `MDATA_DOWNLOAD` string decides what happens.
With `ask`, the default, an interactive XSPEC session asks whether to
download it, once per command however many files the command turns out to
need; when XSPEC is not reading from a terminal (a script, a pipe, or with
`HEADASNOQUERY` set) nothing is asked and `ask` behaves as
`no`.  With `yes` the file is downloaded without asking, and
with `no` it never is and XSPEC prints the `ftgetmodeldata`
command that would fetch it.  A download is written to a temporary file,
checked against the size and SHA-256 checksum in the catalog, and only then
renamed into place; a file that fails the check is deleted, and Ctrl-C
abandons a download.  Files are only ever downloaded into the model data
directory, never into a directory named by one of the model-specific
`*_DIR` strings below.  The three settings can also be given in
`Xspec.init`:

```
XSPEC> xset MDATA_DOWNLOAD yes
   // download missing model data files without asking
XSPEC> xset MDATA_REMOTEDIR https://my.mirror/xspec/modelData
   // fetch them from a mirror
```

The `seed` option requires an integer argument,
which will then be used to immediately re-seed and re-initialize XSPEC's
random-number generator.

The `delta` option is for setting fit delta values (see the `newpar` 
command) which are proportional to the current parameter value rather than 
fixed.  For example,

```
XSPEC> xset delta .15
```

will set each parameter fit delta to .15 * parVal.  To turn proportional 
deltas off and restore the original fixed deltas, set `delta` 
to a negative value or 0.0.  The current proportional delta setting can 
be seen with `show control`.  The inputs of a neural-network table
model (see `atable`) are an exception: they always step by their own
fit delta, initially the table file's DELTA value, whatever this setting.

The `usechainrule` option can be used
to switch between the fast (usechainrule yes) and slow (usechainrule
no) options when calculating the derivatives of the fit statistic.

The `<string_name>` option can be used to pass string values to models. 
XSPEC maintains a database of `<string_name>`, `<string_value>` 
pairs created using this command. Individual model functions can then access 
this database. Note that `xset` does no checking on whether the 
`<string_name>` is used by any model so spelling errors will not be trapped.

To access the `<string_name>`, `<string_value>` database from 
within a model function use the fortran function `fgmstr`. This is 
defined as `character*128` and takes a single argument, the string 
name as a `character*128`. If the `<string_name>` has not been 
set then a blank string will be returned.

In addition to the model control strings
listed further below, a number of operational switches use the same
database mechanism.  These are toggled with

```
XSPEC> xset CONTROL_STRING yes
```

where the value may be any of `yes/no/on/off/true/false/1/0`
(case-insensitive).  Each defaults as the table says, and as a bare
`xset` lists it, and a change takes
effect immediately -- there is no need to reload data or models.  The
switches whose names end in `_CROSS` or `_SELFTEST`
are validation aids: they run two independent implementations of the
same calculation and warn if the results disagree, at some cost in
speed.  The `DISABLE_` switches revert an optimized numerical
path to its slower reference implementation.

{{1.5}
|p{0.42}|}

ANALYTIC_GRAD & How leven and migrad fits get the derivatives of
the fit statistic: `auto` (the default), `always` or
`never`.  With `always` every component that has an
analytic gradient uses it; with `never` all derivatives are finite
differences.  With `auto` a component whose analytic gradient costs
more than finite differences of its free parameters uses finite
differences instead, and only the free parameters' gradient columns are
computed and folded through the response.  At present only table models
(interpolated and neural-network) report such a cost, so under
`auto` their parameters use finite differences in leven fits (see
`atable`); every other component is treated as under
`always`.  Migrad keeps every analytic gradient under
`auto`, computing columns only for free parameters, since it stops
where the gradient it is given vanishes and a finite-difference gradient
can vanish short of the minimum.  The value is case-insensitive; any
other value means `auto`, with a warning.  HMC ignores this
switch.

DISABLE_ANALYTIC_GRAD & Revert leven and migrad fits to
finite-difference derivatives of the fit statistic even when every
active model component has a registered analytic gradient.  Equivalent
to `ANALYTIC_GRAD never` and takes precedence over any
`ANALYTIC_GRAD` value.  Useful to
reproduce fit results from versions before analytic gradients were
introduced, or to test whether a change in a fit result is due to
derivative accuracy.  HMC always uses its own analytic path and
ignores this switch.

HYBRID_GRAD_CROSS & In leven fits, calculate the fit derivatives with
both the analytic path and finite differences at every iteration and
print a comparison, with per-parameter detail at higher chatter
levels.  The fit itself proceeds with the analytic result.

TABLE_NODE_POLISH & Set to `no` to stop `fit` trying a free
interpolated-table parameter that ends within its fit delta of a grid node
held on that node (see `fit`).  On by default.

LM_DELTA_ESCALATE & Set to `off` to stop leven fits retrying a
zero finite-difference derivative with a larger step.  When a parameter's
finite-difference derivative is exactly zero --- usually because the step is
too small for the model to change, as for a narrow line moving inside one
energy bin --- the fit tries the step $\times 10$, up to three times (never
more than 1% of the parameter's hard range), before pegging the parameter
as insensitive.  The larger step lasts for that fit only; the parameter's
delta is not changed, and each new `fit` (and each fit inside
`error` or `steppar`) starts from it again.  Analytic
derivatives and migrad fits are never affected.  An escalation is reported at
chatter 10, and a parameter pegged after one says how far its step was
raised.  On by default.  PyXspec: `Fit.deltaEscalation`.

LIMIT_POLISH & Set to `no` to stop `fit` trying a free
parameter that ends within its fit delta of a hard limit held on that
limit (see `fit`).  On by default.

ERROR_SEARCH & How `error` searches for a confidence bound:
`newton` (the default) or `classic` (the search of earlier
versions).  See `error` and Appendix AppendixAlgorithmsErrorSearch.
`save` writes the setting only for `classic`.  PyXspec:
`Fit.errorSearch`.

LEVEN_PARALLEL & `auto` (the default): `parallel leven`
sets a ceiling, and each fit times its first set of derivatives both in the
subprocesses and in the main process, using the subprocesses only if that is
more than 10% quicker, and checks again every 20 iterations.
`forced`: always use the subprocesses.  The fit is the same either
way.  See `parallel`.

PARALLEL_TIMING & Report how each pool of parallel subprocesses performed
(see `parallel`): `yes` prints a report as each pool closes,
`<file>` appends one line of JSON per pool to `<file>`,
`yes,``<file>` does both, and `no` (the default)
neither.  `tclout` `parallel timing` returns the last pool's
numbers.

SHARED_RMF_FOLD & Set to `off` to fold every source of a spectrum
through its own response separately.  By default sources of one spectrum
whose responses use the same RMF are folded together, the RMF applied once to
the sum of their ARF-weighted model spectra
(Appendix AppendixAlgorithmsSharedRmf).  The results are the same up
to the order of summation (about $10^{-15}$ relative).  On by
default.

DISABLE_VJP & Replace the fused vector-Jacobian product
used for HMC gradients with the explicit
Jacobian-then-multiply path.  Intended for comparing the two analytic
implementations.

INPUT_CHECK & What XSPEC does with a response, ARF or table model file
that fails the checks made as the file is read
(Appendix AppendixAlgorithmsInputChecks): `on` (the default)
refuses the file, as if it could not be read; `warn` loads it with a
warning, for a broken file that has to be used anyway.  Problems XSPEC can
correct in memory, and lesser ones, are warnings either way.  Applies to
files read from then on.  Any other value means `on`, with a
warning.  PyXspec: `Xset.inputCheck`.

TABLE_INTERP & How table models (`atable`, `mtable`,
`etable`, `ctable`) interpolate between their tabulated parameter values:
`auto` (the default) follows each parameter's INTORDER column in the
file, linear where there is none; `linear` interpolates every
parameter linearly; `pchip` interpolates every parameter with three or
more tabulated values by monotone cubic (PCHIP), which is smooth across the
grid nodes and never overshoots (see `atable`).  Setting it recomputes
the models.  Any other value means `auto`, with a warning.  PyXspec:
`Xset.tableInterp`.

VJP_SELFTEST & At the start of an HMC run, cross-check
the vector-Jacobian product against the product of the full Jacobian
with a random adjoint vector for each active model, and refuse to run
HMC if they disagree.  Intended for use when developing new model
gradient functions.

VJP_CROSS & At every HMC gradient call compute both the
vector-Jacobian product and a finite-difference estimate and warn on
disagreement.  More exhaustive, and considerably more expensive, than
VJP_SELFTEST.

SVD_CROSS & For responses using the low-rank
(SVD) convolution path, also run the exact matrix multiplication on
every call and warn if the two disagree beyond the expected
reconstruction accuracy.

DISABLE_CONVOLVEMANY & Revert the
batched convolution of analytic-gradient Jacobian columns to the
legacy one-column-at-a-time
loop.  Intended for benchmarking only.

CONVOLVEMANY_CROSS & Cross-check the
batched convolution of analytic-gradient Jacobian columns against the
one-column-at-a-time loop on every
gradient call and warn on the first disagreement.

DISABLE_COMPONENT_CACHE & Recompute every model
component on each evaluation instead of reusing cached component
results.

COMPONENT_CACHE_CROSS & Recompute model components in a
scratch buffer and verify that the cached result matches.

ARF_PREBAKE_CROSS & Cross-check the prebaked
response-times-ARF fast path against a live multiplication by the
ARF.

}

The current `<string_name>` options, models to which they apply and
brief descriptions are given in the following table :

{{1.5}
|p{0.3}|p{0.3}|}

APECROOT or SPEXROOT & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)expcheb6, (b)(v)(v)gadem,
(v)mekal, mkcflow, nlapec, (b)snapec, (b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Switch from default AtomDB or SPEX input files.

APECTHERMAL or SPEXTHERMAL & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Thermally broaden emission lines in APEC or SPEX input files.

APECVELOCITY or SPEXVELOCITY & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Velocity broaden emission lines in APEC or SPEX input files.

APECMINFLUX or SPEXMINFLUX & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Set minimum flux for line broadening when using APEC or SPEX input files.

APECBROADPSEUDO or SPEXBROADPSEUDO & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Broaden pseudo-continuum lines when using APEC or SPEX input files.
 
APECNOLINES or SPEXNOLINES& (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Continuum only when using APEC or SPEX input files.
 
APECREMOVELINES & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, mkcflow, (b)(v)(v)nei, (b)(v)(v)npshock,
(b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec, (b)(v)(v)tapec,
rs(v)(v)apec, vmcflow
& Leave out ions or single lines when using APEC input files, e.g.
`"Fe XXV 7 1; Fe XXVI"` (see `apec`).
 
APEC_TRACE_ABUND or SPEX_TRACE_ABUND & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Set trace element abundances when using APEC or SPEX input files.
 
APECLOGTINTERP or SPEXLOGTINTERP & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Use logarithmic interpolation between tabulated temperatures when
using APEC or SPEX input files. 
 
APECMULTITHREAD or SPEXMULTITHREAD & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Parallelize over temperatures when calculating the lines in the
spectrum using the APEC or SPEX input files.

APECEEBREMSS or SPEXEEBREMSS & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Include calculation of the e-e bremsstrahlung when using the APEC or
SPEX input files.

APECDOECOR or SPEXDOECOR & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Include the electron-density correction term (off by default) when
using the APEC or SPEX input files.

APECUSESPEX & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)expcheb6, (b)(v)(v)gadem,
(v)mekal, mkcflow, nlapec, (b)snapec, (b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Switch from APEC to SPEX input files but apply all other APEC settings.

APECUSENEI & (b)(v)(v)apec, c6(v)mekl, c6pmekl, c6pvmkl, cemekl, cevmkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)coolflow, (b)(v)(v)wdem, (b)(v)expcheb6, (b)(v)(v)gadem,
(v)mekal, mkcflow, nlapec, (b)snapec, (b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Use NEI code to calculate CEI spectra.

APECEIGENFILE & (b)(v)equil, (b)(v)(v)gnei, (b)(v)(v)nei,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov
& Switch from default AtomDB NEI eigenvector file.

MIXMATRIX_FILE & mixmatrix & The file of mixing weights.

MDATA_CATALOG & all models with model data files & Catalog of
downloadable model data files.  The default is
`modelDataFiles.csv` in the `spectral/manager`
directory.

MDATA_DOWNLOAD & all models with model data files & What to do when a
catalogued model data file is missing: `ask` (the default),
`yes` or `no`.  See above.

MDATA_REMOTEDIR & all models with model data files & Where missing
model data files are downloaded from.  The default is
`https://heasarc.gsfc.nasa.gov/FTP/software/xspec/spectral/modelData`.

NEIAPECROOT & (b)(v)equil, (b)(v)(v)gnei, (b)(v)(v)nei,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov
& Switch from default AtomDB NEI input files.

NEIVERS & (b)(v)equil, (b)(v)(v)gnei, (b)(v)(v)nei,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov
& Select the AtomDB NEI version. Ignored (with a warning) if NEIAPECROOT
is also set.

NEI_TRACE_ABUND & (b)(v)equil, (b)(v)(v)gnei, (b)(v)(v)nei,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov
& Set the trace element abundances for the NEI models (the NEI
counterpart of APEC_TRACE_ABUND). Value is a number or an element
symbol whose abundance the trace elements follow.

NSA_FILE & nsa & Change filename used for model data.

NSAGRAV_DIR & nsagrav & Change directory used for model data files.

NSMAX_DIR & nsmax & Change directory used for model data files.

NSMAXG_DIR & nsmaxg & Change directory used for model data files.

NSX_DIR & nsx & Change directory used for model data files.

POW_EMIN, POW_EMAX & powerlaw, bknpower, bkn2pow, cutoffpl & Switch to 
normalize to a flux calculated over an energy range.

CARBATM & carbatm & Switch the directory for the input file.

CFLOW_VERSION & mkcflow, vmcflow & Switch  CFLOW version number.

CFLOW_NTEMPS & mkcflow, vmcflow & Switch  number of temperature bins 
used in CFLOW model.

HATM & hatm & Switch the directory for the input file.

ISMABSROOT & ismabs & Directory for the ismabs input data files.

ISMDUSTROOT & ismdust, olivineabs & Directory for the ismdust and
olivineabs input data files.

TBABSVERSION & tbabs, tbfeo, tbgas, tbgrain, tbpcf, tbrel, tbvarabs
& Select the version of the TBabs cross-sections and ISM abundances
(1 for the original, 2 for the default).

LINECRITLEVEL & gaussian, Lorentzian and Voigt emission- and
absorption-line models, gsmooth, lsmooth, rsgauss, feklor, fekblor
& Set the critical flux level down to which the line profiles are
calculated, overriding each model's built-in default.  For the emission
lines this is the largest fraction of the line flux allowed outside the
calculation window; Lorentzian and Voigt lines are renormalized to the flux
inside it, and Gaussian lines are never cut closer than six sigma.

IREFLECT_MAX_E & ireflect & Set the maximum energy for which to
calculate the output spectrum.

IREFLECT_PRECISION & ireflect & Set the fractional precision for the Greens'
function adaptive integration.

REFLECT_MAX_E & reflect & Set the maximum energy for which to
calculate the output spectrum.

REFLECT_PRECISION & reflect & Set the fractional precision for the Greens'
function adaptive integration.

RFXCONV_DIR & rfxconv & directory to use for input model data files instead of
the standard modelData directory.

RFXCONV_MAX_E & rfxconv & the maximum energy for which to calculate the
output spectrum.

RFXCONV_PRECISION & rfxconv &  precision used in adaptive Gauss-Kronrod
quadrature of the Greens' function integral.

RGS_XSOURCE_FILE & rgsext, rgsxsrc & set the file from which to read
the image filename, boresight and extraction information.

SUZPSF-IMAGE & suzpsf & Set image file to be used for surface brightness.

SUZPSF-RA & suzpsf & Set RA for center surface brightness map which is 
taken from the WMAP.

SUZPSF-DEC & suzpsf & Set Dec for center surface brightness map which is 
taken from the WMAP.

SUZPSF-MIXFACT-IFILE# & suzpsf & Set filename to read mixing factors.

SUZPSF-MIXFACT-OFILE# & suzpsf & Set filename to write mixing factors.

XILCONV_MAX_E & xilconv & maximum energy for which to calculate the output spectrum.

XILCONV_PRECISION & xilconv & precision used in adaptive
Gauss-Kronrod quadrature of Greens' function integral.

SLIMBB_DIR & slimbh & directory to use for the input table instead of the
standard modelData directory.

SLIMBB_TABLE & slimbh & name of the input table file (default
{ slimbb-full.fits}).

XILCONV_DIR & xilconv & directory to use for ionization model filenames instead of
the standard modelData directory.

XILCONV_VERSION & xilconv & version number of the xillver file,
options are 3 and 5 (the default).

XMMPSF-IMAGE & xmmpsf & Set image file to be used for surface brightness.

XMMPSF-RA & xmmpsf & Set RA for center surface brightness map which is 
taken from the WMAP.

XMMPSF-DEC & xmmpsf & Set Dec for center surface brightness map which is 
taken from the WMAP.

XMMPSF-MIXFACT-IFILE# & xmmpsf & Set filename to read mixing factors.

XMMPSF-MIXFACT-OFILE# & xmmpsf & Set filename to write mixing
factors.

XSCAT_DIR & xscat & Change directory used for model data files.

ZXIPCF_DIR & zxipcf & Change directory used for model data files.

}

**Examples:**

```
XSPEC> xset NEIAPECROOT 2.0
   // Set the NEIAPECROOT variable to 2.0
XSPEC> xset 
   // List the current string variables
XSPEC> xset apecroot /foo/bar/apec_v1.01
   // Set the APECROOT variable
XSPEC> xset seed 1515151
   // Re-initialize the pseudo random-number generator
   // with the seed value 1515151
```
