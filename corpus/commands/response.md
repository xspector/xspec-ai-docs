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
XSPEC12> response a,b,c         
// New files for the response are given for all three files.
XSPEC12> response 2 none        
// No response will be used for the second file.
XSPEC12> response ,d{2}         
// The second response in d becomes the response for 
//the second file.
```

Multiple source usage:

```
XSPEC12> response 2:1 e
// A second source with response e.rsp is now added to  
// the first spectrum.  A second model can be assigned 
// to this source.
XSPEC12> response 2:2 f  3:2 g                
// A second and third source is assigned to spectrum 2.
XSPEC12> response 2:2 none                  
// The second source is now removed from spectrum 2.
```
