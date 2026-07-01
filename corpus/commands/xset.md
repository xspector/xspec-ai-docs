---
name: xset
aliases: [xxset]
also_documents: [xsetdelta, xsetseed]
source: XSxset.tex
---

# xset

**set variables for XSPEC models**

Modify a number of XSPEC internal switches.

**Syntax:** `xset` [abund | cosmo | delta | 
mdatadir | method | seed | statistic | usechainrule
| weight | xsect | <string_name> ]
[ <options> | <string_value> ]

The arguments `abund, cosmo, method, statistic, weight`, and `xsect` 
just run the appropriate XSPEC commands. `mdatadir` changes the 
directory in which XSPEC searches for model data files. You probably don't 
want to change this.  The `seed` option requires an integer argument,
which will then be used to immediately re-seed and re-initialize XSPEC's
random-number generator.

The `delta` option is for setting fit delta values (see the `newpar` 
command) which are proportional to the current parameter value rather than 
fixed.  For example,

```
XSPEC12> xset delta .15
```

will set each parameter fit delta to .15 * parVal.  To turn proportional 
deltas off and restore the original fixed deltas, set `delta` 
to a negative value or 0.0.  The current proportional delta setting can 
be seen with `show control`.

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

The current `<string_name>` options, models to which they apply and 
brief descriptions are given in the following table :

{{1.5}
|p{0.3}|p{0.3}|}

APECROOT or SPEXROOT & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)expcheb6, (b)(v)(v)gadem,
(v)mekal, mkcflow, nlapec, (b)snapec, (b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Switch from default AtomDB or SPEX input files.

APECTHERMAL or SPEXTHERMAL & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Thermally broaden emission lines in APEC or SPEX input files.

APECVELOCITY or SPEXVELOCITY & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Velocity broaden emission lines in APEC or SPEX input files.

APECMINFLUX or SPEXMINFLUX & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Set minimum flux for line broadening when using APEC or SPEX input files.

APECBROADPSEUDO or SPEXBROADPSEUDO & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Broaden pseudo-continuum lines when using APEC or SPEX input files.
 
APECNOLINES or SPEXNOLINES& (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Continuum only when using APEC or SPEX input files.
 
APEC_TRACE_ABUND or SPEX_TRACE_ABUND & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Set trace element abundances when using APEC or SPEX input files.
 
APECLOGINTERP or SPEXLOGINTERP & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Use logarithmic interpolation between tabulated temperatures when
using APEC or SPEX input files. 
 
APECMULTITHREAD or SPEXMULTITHREAD & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Parallelize over temperatures when calculating the lines in the
spectrum using the APEC or SPEX input files.

APECEEBREMSS or SPEXEEBREMSS & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)equil, (b)(v)expcheb6,
(b)(v)(v)gadem, (b)(v)(v)gnei, (v)mekal, mkcflow, (b)(v)(v)nei, nlapec,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov, (b)snapec,
(b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Include calculation of the e-e bremsstrahlung when using the APEC or
SPEX input files.

APECUSESPEX & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)(v)cie, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)expcheb6, (b)(v)(v)gadem,
(v)mekal, mkcflow, nlapec, (b)snapec, (b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Switch from APEC to SPEX input files but apply all other APEC settings.

APECUSENEI & (b)(v)(v)apec, c6(v)mekl, c6p(v)mekl, ce(v)mkl, (b)(v)cempow,
(b)(v)cheb6, (b)(v)coolflow, (b)(v)(v)dem, (b)(v)expcheb6, (b)(v)(v)gadem,
(v)mekal, mkcflow, nlapec, (b)snapec, (b)(v)(v)tapec, rs(v)(v)apec, vmcflow
& Use NEI code to calculate CEI spectra.

APECEIGENFILE & (b)(v)equil, (b)(v)(v)gnei, (b)(v)(v)nei,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov
& Switch from default AtomDB NEI eigenvector file.

NEIAPECROOT & (b)(v)equil, (b)(v)(v)gnei, (b)(v)(v)nei,
(b)(v)(v)npshock, (b)(v)(v)pshock, (b)(v)(v)rnei, (b)(v)(v)sedov
& Switch from default AtomDB NEI input files.

NSA_FILE & nsa & Change filename used for model data.

NSAGRAV_DIR & nsagrav & Change directory used for model data files.

NSMAX_DIR & nsmax & Change directory used for model data files.

NSMAXG_DIR & nsmaxg & Change directory used for model data files.

NSX_DIR & nsx & Change directory used for model data files.

POW_EMIN, POW_EMAX & powerlaw, bknpower, bkn2pow, cutoffpl & Switch to 
normalize to a flux calculated over an energy range.

CARBATM & carbatm & Switch the directory for the input file.

CFLOW_VERSION & mkcflow, vmclow & Switch  CFLOW version number.

CFLOW_NTEMPS & mkcflow, vmclow & Switch  number of temperature bins 
used in CFLOW model.

HATM & hatm & Switch the directory for the input file.

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

SUZSF-MIXFACT-OFILE# & suzpsf & Set filename to write mixing factors.

XILCONV_MAX_E & xilconv & maximum energy for which to calculate the output spectrum.

XILCONV_PRECISION & xilconv & precision used in adaptive
Gauss-Kronrod quadrature of Greens' function integral.

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
XSPEC12> xset NEIAPECROOT 2.0
   // Set the NEIAPECROOT variable to 2.0
XSPEC12> xset 
   // List the current string variables
XSPEC12> xset apecroot /foo/bar/apec_v1.01
   // Set the APECROOT variable
XSPEC12> xset seed 1515151
   // Re-initialize the pseudo random-number generator
   // with the seed value 1515151
```
