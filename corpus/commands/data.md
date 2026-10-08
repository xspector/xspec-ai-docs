---
name: data
aliases: [xdata]
also_documents: []
source: XSdata.tex
---

# data

**read data, background, and responses**

Input one or more spectra, together with their associated (background, response) files.

 p{} p{---6}}
**Syntax:** & **data** & `<file spec1> [,...] [<file spec2>...] [/]`

                 & **data** & `none`

                 & **data** & `<spectrum #>  none`

where the file specification is

`<filespec>` ::= [[`<data group #>`:] `<spectrum #>`] `<filename>` [`{ranges}`]

If a particular file is not found or cannot be opened for input for some reason, 
then the user is prompted for a replacement file name. An <EOF> at this point 
is equivalent to typing `none`. The default extension for all files is 
`.pha`, so all other extensions, (e.g. `.fak`) must be entered 
explicitly. The default directory is the current user directory when XSPEC is 
invoked. When a new file is input, by default all its PHA channels are 
considered good channels for fitting and plotting purposes (see the `ignore` 
and `notice` commands).

XSPEC's ``native'' data format is the OGIP standard. The standard specifies the 
representation of spectrum and all related datasets. XSPEC12 is explicitly 
designed to be able to work with other data formats as required: for example, 
the Integral/SPI spectral data format, although based on OGIP Type II, deviates 
slightly. This was necessary because 3 response/arf pairs are required per 
spectrum. XSPEC12 has the ability to specify how response and other data are 
stored on disk, composed, and combined within the spectral fitting problem by 
adding new data modules at run-time. In XSPEC12, unlike XSPEC11, the channels 
that are ignored are a property of the spectrum, and therefore must be reset 
when the spectrum is replaced by another.

If the file contains multiple spectra, such as an OGIP Type II PHA file, then 
the desired spectrum can be specified by appending `{ranges}` to the 
end of the filename, where n is the row number of the spectrum in the file. 

XSPEC12 allows any combination of multiple ranges in the parentheses delimited 
by commas. The wildcard characters * and ** may also be used.  A ** on either 
side of a hyphen indicates either the first or last row in the file, based 
on whether it is to the left or right of the hyphen.  (If a * is entered on 
the left or right side of a hyphen, it is substituted by the most recently 
entered left or right value respectively.)  All rows in the file may be selected 
simply with a single * or ** between the brackets with no hyphen.

The output displays the net count rate (in cts/s) +/- the uncertainty 
(uncertainty = square root of the variance). These values can also be retrieved in a script with 
the `tclout` `rate` command. 

**Examples:**

```
XSPEC> data pha2data{1,3,5-8,14-26,75-**}
//  In addition to the various specified rows between 1 and 26, 
//  also load rows 75 through the end of the file.
XSPEC> data pha2data{*}
//  Select all rows in the file.
```

For files with multiple spectra the data may either specify a header keyword 
specifying the response, auxiliary response, background and correction files, 
or these may be string-valued columns specifying a different filename per row.

Consult the http://heasarc.gsfc.nasa.gov/docs/software/ftools package
documentation for details of how to modify the file.

The individual spectral data files are created outside of XSPEC by 
detector-specific software. They are organized as XSPEC data files, but often 
referred to as PHA files. Whatever its format, the PHA file contains such 
information as integration time, detector effective area, and a scaling 
factor (BACKSCAL in the OGIP standard) that estimates the expected size of the 
internal background. The data file also contains the names of the default files 
to be used for background subtraction and for the detector sensitivity versus 
incident photon energy (the response and arf files). A data file has the total 
observed counts for a number of channels and a factor for the size of any 
systematic error. Each channel is converted to a count rate per unit area 
(assumed $cm^{-2}$). The default background file is used for background subtraction. 
An error term is calculated using Poisson statistics and any systematic error 
indicated in the file.For OGIP files, any FITS NULL values will be 
converted to the value 1.E-32. This should have no practical effect because 
any channels with NULL values will presumably be marked as bad or otherwise ignored.

**spectrum numbering**

Multiple `<filespec>` clauses can be input on a single data command, or 
also on multiple data commands. Within XSPEC each set of data is referred 
to by its associated spectrum number,`<spectrum #>`, as determined by the 
following rules. For convenience, we denote the number of spectra that have 
been previously read in by data command as $N_{s}$.

Spectra in XSPEC are numbered sequentially from 1. 

If no spectrum number is specified by the user, the spectrum in the first 
filename specified is assigned to 1. If spectra have already been loaded at 
this point, they will be replaced, deleted, or added to depending on the 
command. For example, if there are 3 spectra loaded ($N_{s}$ = 3) and the user types:

```
XSPEC> data   multidatafile{1-2}
```

then spectra 1 and 2 will be replaced and 3 deleted. The command

```
XSPEC> data   multidatafile{1-4}
```

will replace all three spectra and add the fourth.

If the user specifies a ``load point'', 
i.e. the first spectrum number to be created by the new command, i.e.

```
XSPEC> data 3 multidatafile{1-4}
```

then that load point may not exceed $N_{s}$ + 1. If it does, XSPEC will correct 
the number and issue a warning.

A skipped-over argument can be effected by a comma, for example

```
XSPEC> data  3 spectrum1, , spectrum2
```

indicates that the spectrum for that position, as input in an earlier invocation 
of data,  will continue to be used (in this example, spectrum 3 is replaced, 
4 is left untouched, and 5 is either replaced or added. Any spectra with 
numbers greater than 5 are removed.

If the filename input is `none`, that spectrum is removed, and so are any 
higher-number spectra unless `none` is terminated with a / character. 
For example:

```
XSPEC> data  3 none
```

removes all spectra numbered 3 or higher,

```
XSPEC>data 3 none/
```

removes only spectrum 3 and renumbers the rest.

The data command determines the current total number $N_{T}$ of spectra: 
either $N_{T}$ spectra are implied by the command line, or the highest spectrum 
number added (after XSPEC has made corrections as mentioned above) is $N_{T}$ 
This is true UNLESS a  / character terminates the data command.

If the line is terminated by a slash (/), then the current number of spectra 
is the previous total number of datsets $N_{s}$ or the number as determined 
from the command line, whichever is greater.

The command 

```
XSPEC> data 
```

by itself prints the one-line help summary, as does

```
XSPEC> data ?
```

**data groups**

XSPEC allows the user to specify separate data groups for different spectra. 
Each data group has its own set of parameters for the defined model. These 
parameters can be either independent from data group to data group, or they 
can be linked across data groups using the standard XSPEC syntax (see the 
`newpar` command). This facility can be used for, say, analyzing extended sources.

Note that the data group number precedes the spectrum number: in the example

```
XSPEC> data  2:3 spectrum4
```

which assumes that at least two spectra are already present, the data group 
number is 2 and the spectrum number is 3. 

XSPEC will not allow the data group number to exceed the spectrum number: for example

```
XSPEC> data  3:2 spectrum4
```

is invalid. XSPEC will correct this and issue a warning.

**More Examples:**

```
XSPEC> data a
//The file a.pha is read in as the first (and only) spectrum.
XSPEC> data ,b
//b.pha becomes the second spectrum, the first spectrum is
// unmodified (i.e. it is still a.pha)
XSPEC> data c 3 d,e,f
//c.pha replaces a.pha as the first spectrum;d.pha, e.pha, and 
// f.pha provide the, third, fourth, and fifth spectra.
XSPEC> data g/
//g.pha replaces c.pha as the first spectrum; the slash (/)
// indicates that the 2nd through the 5th spectra remain as before.
XSPEC> data 2 none/
//the string none indicates that the 2nd spectrum (b.pha) is to be 
// totally removed. The current total number of datasets thus becomes 
// one less (4).The current spectra are g.pha,d.pha, e.pha,
// and f.pha.
XSPEC> data h,,
//The current total number of spectra becomes 2, the current data 
// sets are from h.pha and d.pha.
XSPEC> data
//There is no change in the data status.
XSPEC> data 1
//The number of spectra is set explicitly to one, that being from 
// h.pha.
XSPEC> data 1:1 a 2:2 b 3:3 c
//Read a.PHA into data group 1, b.pha into data group 2, and c.pha 
//into data group 3
XSPEC> data 1:1 a 1:2 b 2:3 c
//Read a.pha and b.pha into data group 1, and c.pha into data group 2
XSPEC> data a{3}
// Read the third spectrum in the file a.pha.
```
