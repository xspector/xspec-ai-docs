---
name: corfile
aliases: [xcorfile]
also_documents: []
source: XScorfile.tex
---

# corfile

**change the correction file for a given spectrum**

Reset the files used for background correction.

**Syntax:** `corfile` [<filespec>...]

where `<filespec>` is the same as for the `backgrnd`
command.  The correction file can be associated with a spectrum to
further adjust the count rates. It is a PHA file whose count rate is
multiplied by the current associated correction norm (see the
`cornorm` command and `recorn` model) and then subtracted
from the input uncorrected data. The correction norm is not changed by
running the `corfile` command. Default values for the correction
file and norm are included in the data PHA file. Unlike the background
file, the correction data does NOT contribute to the measurement
error. A file name of `none` is equivalent to no correction
file used.  If an input file can not be opened or found, an error
message is printed and the user prompted for a replacement. As with
the `backgrnd` command, the correction file is checked against
the associated spectrum for number of channels, grouping status, and
detector ID. The current ignore status for channels is not affected by
the `corfile` command. Note that correction files have the same
format as the PHA files used by the `data` command.

**Examples:**
  
It is assumed that there are currently three spectra:

```
XSPEC12> corfile a,b,c
// New correction files are used for all three spectra.>
XSPEC12> corfile 2 none
// No correction will be done for the second spectrum.}
XSPEC12> corfile ,d
// The 2nd file now uses d.pha as its correction.
XSPEC12> corfile 2 e{4-5}
// Rows 4 and 5 of Type II file e.pha become the correction files 
// for the second and third spectrum respectively.
```
