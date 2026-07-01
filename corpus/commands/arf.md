---
name: arf
aliases: [xarf]
also_documents: []
source: XSarf.tex
---

# arf

**change the efficiency file for a given response**

Read in one or more auxiliary response files (ARF). An ARF gives area 
versus energy and is used to modify the response matrix for a spectrum. 
The file must be in the OGIP standard format.

**Syntax:** `arf` [<filespec>...]

where `<filespec>` ::= [[`<source #:>`]`<spectrum num>`]  
`<filename>`[{ranges}]... and where `<spectrum num>` is the spectrum 
number for the first `<filename>` specified, `<spectrum num>` 
plus one is the spectrum number for the next file (or next entry in {ranges} 
specifier for Type II multi-ARF files), and so on.  `<filename>` is the 
name of the auxiliary response file to be used with the associated spectrum.  
The optional source number defaults to 1, and for ARFs stored in OGIP Type II 
files, {ranges} specifies the row numbers of the desired ARF(s).  See the 
`data` command for allowed range specification.

If no `<spectrum num>` is given in the first `<filespec>` it is 
assumed to be 1. If no file specifications are entered, then none of the 
spectrum responses are modified.An error message is printed if the spectrum 
number is greater than the current number of spectra (as determined from 
the last use of the `data` command). A file name `none` indicates 
that no auxiliary response is to be used for that spectrum. If a file is not 
found or cannot be opened for input, then the user is prompted for a 
replacement auxiliary response file. An <EOF> at this point is equivalent 
to `none`. See the `data` command for ways to completely remove 
the dataset from consideration.

Note: The `arf` command is currently not implemented for data formats 
which use multiple RMFs per spectrum, such as Integral/SPI data. 

**Examples:**
  
It is assumed that there are currently three spectra:

```
XSPEC> arf a,b,c
// New files for the auxiliary response are given for all 
// three spectra.
XSPEC> arf 2 none
// No auxiliary response will be used for the second spectrum.
XSPEC> arf ,d.fits
// d.fits becomes the auxiliary response for the second spectrum.
XSPEC> arf 2 e.fits{3-4}
// Rows 3 and 4 of multi-ARF file e.fits become the auxiliary 
// responses for the second and third spectra.
XSPEC> arf 2:1 f.fits
// f.fits becomes the auxiliary response for the second source of 
// spectrum 1.
```
