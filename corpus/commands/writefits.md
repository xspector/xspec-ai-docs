---
name: writefits
aliases: []
also_documents: []
source: XSwritefits.tex
---

# writefits

**write information about the current fit and errors to a FITS file**

Tcl script to dump a lot of useful information to a FITS file. 

**Syntax:** `writefits`   <FITS filename>

This script writes filenames, free parameter values and errors to one row of 
a FITS file. The error command should have been run on all the free parameters 
before running this script. If the FITS file already exists then a new row 
is appended.
