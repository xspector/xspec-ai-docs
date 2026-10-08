---
name: backgrnd
aliases: [xbackgrnd]
also_documents: []
source: XSbackgrnd.tex
---

# backgrnd

**change the background file for a given spectrum**

Modify one or more of the files used in background subtraction.

 p{} p{---6}}
**Syntax:** & **backgrnd** & `[<filespec>...]`

                 & **backgrnd** & `<spectrum number>  none`

where `<filespec>` ::= [`<spectrum num>`]  `<filename>`... and where 
`<filename>` is the name of the PHA file to be used for background 
subtraction. The numbering scheme is as described for the `data` command, except 
that the `<spectrum num>` must have previously been loaded.

An error message is printed if  `<spectrum num>` is greater than the 
current number of spectra (as determined from the last use of the `data` command). 
`backgrnd` `<n>` `none` indicates that no background 
subtraction is to be performed for that spectrum. If a file is not found or 
cannot be opened for input, then the user is prompted for a replacement 
background file (an <EOF> at this point is equivalent to `backgrnd`
`<spectrum number>` `none`). The current ignore status for 
channels is not affected by the `backgrnd` command. (See the `ignore`
and `notice` commands). Finally, any grouping specification will be 
overridden by the grouping in the source spectral file so that the source 
and background are binned in the same way. 

The format of the background file must match that of the spectrum file: for 
this purpose OGIP Type I and II are considered to be the same format.

For details of how to remove spectra see the `data` command documentation.

**Examples:**
  
Suppose there are currently three spectra.  Then:

```
XSPEC> backgrnd a,b,c
// New files for background subtraction are given for all 
// three spectra.
XSPEC> backgrnd 2 none
// No background subtraction will be done for the second spectrum.
XSPEC> backgrnd ,d
// d.pha becomes the background for the second spectrum. 
XSPEC> backgrnd 2 e{4-5}
// Rows 4 and 5 of Type II file e.pha become the background for 
// the second and third spectrum respectively.
```
