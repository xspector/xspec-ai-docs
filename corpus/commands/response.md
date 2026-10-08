---
name: response
aliases: [xresponse]
also_documents: []
source: XSresponse.tex
---

# response

**change the detector response for a spectrum**

Modify one or more of the matrices used to describe the response(s) of the
associated spectrum to incident X-rays.

 p{} p{---6}}
**Syntax:** & **response** & `[<filespec>...]`

                 & **response** & `[<source num>:]<spectrum num>  none`

                 & **response** & `[<source num>:]<spectrum num>  svdrank <K>`

                 & **response** & `[<source num>:]<spectrum num>  svdeps  <eps>`

                 & **response** & `firstorder [[<source num>:]<spectra>]  auto|<k>|off`

where `<filespec>` ::= [[`<source num>`:]`<spectrum
    num>`] `<file name>`..., and `<file name>` is the name of
the response file to be used for the response of the associated
spectrum. If `<file name>` ends in a {n} specifier then the nth
response will be read from the file. If the file contains multiple
responses and no {n} specifier is used then all the responses will
be used together. `<spectrum num>` is the
spectrum number for the first file name in the specification, and
follows similar rules as described in the `data` command
description. An important difference however is that the
`response` command may only be used to modify the response of a
previously loaded spectrum: an error message is printed if the
`<spectrum num>` is greater than the current number of spectra
(as determined from the last use of the `data` command).

Each response is checked as it is read
(Appendix AppendixAlgorithmsInputChecks), and energies in units other
than keV (angstrom, Hz, eV, , as given by TUNIT) are converted to keV
(Appendix AppendixEnergyUnits).  A response with a defect
XSPEC cannot work around --- a NaN energy or matrix element, bins out of
order or overlapping --- is refused unless `xset INPUT_CHECK warn`
is set; a decreasing energy grid or an energy $\le 0$ is corrected in
memory, with a warning.

If the `<file name>` argument is an SVD-K compressed response
side-car (a `.svdmat.fits` file produced by `ftsvdcmprmf`
-- see Appendix AppendixAlgorithmsSVD), the file format is
autodetected and the side-car is attached to the previously-loaded
response without modifying the underlying RMF.  Subsequent
`fit` and `hmc` calls use the rank-$K$ reconstruction
in their convolution kernels.  To switch back to the exact RMF,
re-load the original RMF with another `response` command
(the load installs a fresh response object with empty SVD slots).
The side-car attachment is silent: see `show` `response`
to confirm what is in effect.

Two SVD-K parameter overrides are recognised after a side-car has
been attached:

- `response <spec> svdrank <K>` pins the working
   rank to `<K>` (must be between 1 and the side-car's
   $K_{\mathrm{max}}$).  Use $-1$ to revert to automatic selection
   from the side-car's stored eps-vs-$K$ table.

- `response <spec> svdeps <eps>` pins the target
   Frobenius truncation error to `<eps>`; automatic selection
   then picks the smallest $K$ where eps$_F(K) \leq $ `<eps>`.
   Use $-1$ to revert to the global default ($10^{-4}$).

Neither override survives a re-load of the underlying RMF.

**First-order folding.**
`response firstorder` folds each model energy bin at the mean energy
of its photons rather than at its centre, through the response and its
derivative with energy (Kaastra & Bleeker 2016; see
Appendix AppendixAlgorithmsFirstOrder).  A line near a bin edge, the
worst case for the ordinary fold, is then placed where it is, so a much
coarser model grid gives the same accuracy:

- `response firstorder <k>` merges $k \ge 2$ rows of the
  response into each model bin;

- `response firstorder auto` chooses each bin's width from the
  response's resolution and the spectrum's counts there (the paper's
  Monte Carlo fit for first order);

- `response firstorder off` restores the ordinary fold;

- `response firstorder` with no mode lists each response's
  setting.

`<spectra>` is a spectrum number, a range such as `1-3`, or a
list of those; without it, every response is changed.  `<source num>`
restricts the change to that source's responses.  The change is all or
nothing: if any response cannot be folded first order (a dummy response, a
multiple-RMF response, one with response models such as `gain`
attached, or an SVD-K side-car), none is changed.  The model is then
evaluated on the half-bin grid of the coarse bins (`show response`
gives the numbers of bins before and after), and additive models that supply
their mean photon energies (`moment=1` in `model.dat`: the
line models, `powerlaw`, `bbody`, `bremss` and the
`apec` and `nei` families) are exact within each bin; the
others are folded by a half-bin estimate, and `response`
`firstorder` names them at chatter 10.

A response file written first order --- a `DMATRIX` column beside
`MATRIX` and `RESPORDR = 1`, as written by ftrmf1st
--- is folded first order on its own grid as soon as it is read, and its
grid cannot be changed; `response firstorder off` folds it zeroth
order on that grid, with a warning that the grid assumes first order.  The
setting survives `ignore`, `notice`, a change of grouping and a
new `arf`; loading a new response file, or new data into the slot,
starts it off.  `gain` and the other response models are refused
while first order is on, and first order while they are attached.

An optional `<source num>` may be specified to attach additional responses 
to a spectrum, and should be paired with `<spectrum num>` separated by 
a ':'.  This allows the user to assign multiple models, each with their own 
response file, to a particular spectrum.  See the `model` command for 
more information.  If no `<source num>` is specified, it always defaults 
to 1.  Source numbers do not need to be assigned consecutively to a spectrum, 
and gaps in numbering are allowed.  The additional response may be removed 
with a `response` `<source num>`:`<spectrum num>` `none` 
command.  Both the `show data` and `show response` commands 
will display current information regarding the response(s) to 
spectrum assignments.  

A file name `none` indicates that no response is to be used for that 
spectrum. This situation means that any incident spectrum will produce no 
counts for those particular channels. If a file is not found or cannot be 
opened for input, then the user is prompted for a replacement response file.  
An <EOF> at this point is equivalent to using `none` as the 
response. See the `data` command for ways to totally remove the 
spectrum from consideration. The user is also prompted for a replacement if 
the response file has a different number of PHA channels than the associated 
spectrum. A warning will be printed out if the response detector ID is 
different from the associated spectrum's. The current ignore status for 
channels is not affected by the command. (See the `ignore` and 
`notice` commands).

**Examples:**
  
It is assumed that there are currently three spectra:

Single source usage:

```
XSPEC> response a,b,c         
// New files for the response are given for all three files.
XSPEC> response 2 none        
// No response will be used for the second file.
XSPEC> response ,d{2}         
// The second response in d becomes the response for 
//the second file.
```

Multiple source usage:

```
XSPEC> response 2:1 e
// A second source with response e.rsp is now added to  
// the first spectrum.  A second model can be assigned 
// to this source.
XSPEC> response 2:2 f  3:2 g                
// A second and third source is assigned to spectrum 2.
XSPEC> response 2:2 none                  
// The second source is now removed from spectrum 2.
```

First-order folding:

```
XSPEC> response firstorder 8
// Every response: 8 response rows per model bin.
XSPEC> response firstorder 2-3 auto
// Spectra 2 and 3: bin widths from the resolution and counts.
XSPEC> response firstorder off
// Every response back to the ordinary fold.
```
