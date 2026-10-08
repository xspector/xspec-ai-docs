---
name: fakeit
aliases: [xfakeit]
also_documents: [fakeitnone, fakeitkeywords]
source: XSfakeit.tex
---

# fakeit

**simulate observations of theoretical models**

Produce spectra with simulated data.

**Syntax:** `fakeit` [nowrite] [writersp] [<file spec>...] [<number of spectra>]

**Syntax:** `fakeit` [nowrite] [writersp] [clobber] <keyword>=<value>... [<file spec>...] [<number of spectra>]

where `<file spec>` ::= [`<file number>`] `<file name>`[`{ranges}`]...
is similar to the syntax used in the `backgrnd`, `corfile`, 
and `response` commands. The `fakeit` command is used to create a 
number of spectrum files, where the current model is multiplied by the 
response curves and then added to a realization of any background.  
Statistical fluctuations can be included.

**The file specs on the command line are BACKGROUNDS**, not responses:
`fakeit back.pha` fakes spectrum 1 with back.pha as its
background.  The number of faked spectra produced is the maximum of the
number of spectra currently loaded and the number of file specifications on
the command line, or the trailing `<number of spectra>` if that is
larger.  The special case `fakeit none` makes one fake spectrum for
each spectrum loaded (or one fake spectrum if there are none loaded), with no
background.  See the examples below for a clearer description.

**Answering fakeit's questions.**  For the spectra it is about to make,
`fakeit` needs, in this order: a response and an ARF for each spectrum
that has none of its own; whether to apply counting statistics; an optional
prefix for the output file names; and then, for each output file, its name and
the exposure time, correction norm and background exposure time.  There are
three ways to give them.

- **Prompted** (the default): `fakeit` asks each question in
turn, offering a default in parentheses.

- **``&'' answers**: the answers follow the command, separated by
`&`, in the order above, an empty answer taking the default; for
example `fakeit none & resp.rmf & resp.arf & y & & sim.fak & 1000`.
Miscounting them leaves the remaining questions to be answered from the
terminal (or from the next lines of a script).

- **The keyword form**: any
`<keyword>`=`<value>` argument (or `clobber`) on the command
line means `fakeit` asks nothing at all; whatever is not given takes the
default the prompt would have offered.  It cannot be combined with
``&'' answers.

The keywords are:

}
`response=` & the response file for each spectrum that has no response of its own (the dummy response when not given) 

`arf=` & its ARF, with an optional `{row}` 

`background=` & the background for each fake spectrum, as the positional `<file spec>`s would give it; `none` for no background.  It cannot be given together with positional file specs 

`exposure=` & the exposure time of each output file 

`correction=` & the correction norm of each output file 

`bexposure=` & the background exposure time of each output file 

`stat=` & `yes` (the default) or `no`: whether to apply counting statistics 

`prefix=` & a prefix for the default output file names 

`file=` & the name of each output file 

`seed=` & re-seed the random number generator first, exactly as `xset seed` does 

A value is either one entry, used for every question it answers, or a comma
separated list with exactly one entry per question: one per output file for
`exposure=`, `correction=`, `bexposure=` and
`file=`; one per response asked for (that is, per new spectrum) for
`response=` and `arf=`; one per fake spectrum for
`background=`.  An empty entry keeps that question's default.  A list
of the wrong length is refused, naming the number expected, as is a single
`file=` when there are several output files (use `prefix=`
there), two output files with the same name, a `response=` or `arf=` that no question asks for, and
an unknown keyword.  These checks are made before anything is simulated, so a
refused command changes neither the loaded data nor any file.

With nothing loaded and no `<number of spectra>`, the keyword form makes
one spectrum, as `fakeit none` does.

**Existing files.**  The prompted form asks before overwriting an output
file that already exists; the ``&'' form overwrites it without asking.  The
keyword form refuses, naming the file, if any file it would write (spectrum,
_bkg background, or `writersp` response) already exists,
unless `clobber` is given.  An overwritten file is replaced.

If `writersp` is given and a fake spectrum is folded through a dummy
response (`dummyrsp`, or no data loaded), the dummy response is also
written, to <stem>.rsp beside the output file, and recorded as the
file's RESPFILE, so the fake can be read back without a `dummyrsp`.
This applies to type I output only.

If the `nowrite` specifier is given, no output files are generated.
In this case the fake spectra will exist just for the duration of the Xspec
session (or until they are unloaded).  A fake spectrum keeps its background
in memory, so a further `fakeit` based on it (a simulation loop, for
instance) uses that background even though no background file was written.

To simulate many realizations of the loaded data and collect a statistic from
each, use `sim` instead: it makes its realizations in memory, can refit
each one, and writes no spectrum files.  `fakeit` is for making
spectrum files, or a few spectra to work with by hand.

If a faked spectrum is based on a currently loaded spectrum, then by default 
the background, response, correction file, and numerical information are 
taken from the currently-defined data, unless a background file is specified 
on the command line in which case it becomes the background.  The `fakeit none` 
case prompts for the rmf and arf filenames and sets the default numerical 
data to 1.0, except the correction norm, which is set to zero.  If the
output file is type II then the exposure time and correction scale factor
will be the same for all spectra in the file.

A faked spectrum which is *not* based on a currently loaded spectrum
(ie. one of the extras produced when more fake spectra are requested than are
loaded) has no numerical information of its own, so the exposure time,
correction norm, and background exposure time offered for it default to those
of the preceding output file.  For example, after loading a single spectrum
of 2100 s, `fakeit 2` will offer 2100 s for the second fake spectrum
as well.  If such a spectrum is given a background file on the command line,
that file's exposure time is used for the defaults instead.

For each output file, `fakeit` asks for an output file name.  If 
a background file is in use then `fakeit` will also simulate a new 
background for each spectrum.  Background files are given the same names 
as output spectrum files but with _bkg appended to the end of the stem.

The simulated spectra automatically become the current data files. The 
ignore status is completely reset.

**Statistical Issues:**

The statistical fluctuations used to create the simulated spectra will depend 
on whether the current spectra have Poisson or Gaussian errors. If a 
spectrum file has a STAT_ERR column and the POISSERR keyword is set to false 
then xspec assumes Gaussian errors with sigma from the values in the column. 
Otherwise, errors are assumed to be Poisson based on the number of counts. 
Note that it is possible for the spectrum and background files to have 
different error types. For fakeit cases when there is no current file to use,
Poisson errors are assumed.

If the loaded spectra form a covariance group (Stokes Q/U or I/Q/U carrying
`XCOV` columns, fit with `statistic` `chistokes` or
`chicov`), `fakeit` draws the group's members *jointly* so
the simulated spectra carry the correct per-bin cross-spectrum covariance
rather than independent noise. The group keywords and `XCOV` columns
are propagated to the output spectra; because `fakeit` output is
ungrouped, apply the grouping before fitting the faked data with
`chicov`. See the correlated-spectra discussion in the Statistics
appendix.

**Type I vs. Type II Output:**

Fakeit determines whether to place its fake spectra and background data into 
type I or type II files based on the following rules.

If fake spectra are based on currently loaded spectra then the output files 
will have the same format as those loaded. For example:  Assume 3 spectra are 
currently loaded, spectrum 1 from file typeIdata.pha and spectra 
2 and 3 from file typeIIdata.pha.  Then,

```
XSPEC> fakeit
```

will produce 3 fake spectra in 2 output files with names prompted from the 
user.  The first file will be type I, the second type II containing 2 
spectra.  The same is true for any background files produced.
 
If the user asks for more fake spectra to be created than the number of 
spectra currently loaded,  for example by typing the following when 
the same 3 spectra above described are loaded:

```
XSPEC> fakeit 5
```

then fake spectra 1-3 will be placed in the two files as before.  For the 
additional fake spectra (4 and 5), fakeit uses the following rule:  
If any of the originally loaded spectra were in a type II file, then all 
of the additional fake spectra will be placed in 1 type II file.  Otherwise, 
they will each be placed in a separate type I file.  In this example, since 
a type II file was originally loaded (typeIIdata.pha) when fakeit 
was called, spectra 4 and 5 will be placed together in a type II output file, 
in addition to the type I and type II files for the first 3 fake spectra.  

If there are no currently loaded spectra all output files will be type I 
unless either of the following situations exist:  1.  Any of the background 
files entered on the command line are type II, as indicated by row specifiers 
in brackets.  2.  The first response file used clearly belongs to a format 
associated with type II data, such as SPI/Integral with its multiple RMF 
format (see section on SPI/Integral usage).

Overall, though the method of determining output format for additional 
spectra may seem quite complicated, it can be easily summed up:  Fakeit 
will place all additional spectra and backgrounds (ie. those not based 
on already loaded data) in type I output files, unless it detects any 
evidence of type II file usage amongst the command line input, in which 
case it will produce type II output.

**Note on grouped spectra:**

If an input spectrum has grouping information (ie a GROUPING column telling 
XSPEC how to bin up the data) then fakeit will simulate the number of 
counts in each of the grouped bins. However, the spectrum that is written 
out must have the ungrouped number of channels (and a copy of the GROUPING 
column from the original spectrum). The solution that XSPEC adopts is to 
place all the counts from a grouped bin in the first channel which goes to 
make up that bin. This is of no consequence for future uses of the 
simulated spectrum provided that the GROUPING column is not changed. So, 
in this case ftgrouppha or similar tools cannot be run on the simulated spectrum.
If your simulated spectrum comes from the use of "fakeit none", then the 
spectrum can be grouped with ftgrouppha or simulated tools.

A spectrum faked on a dummy response (`dummyrsp`, or no data loaded)
keeps that dummy as its own response for the rest of the session:
`ignore`, `notice`, `data` and `response` do not
remove it, as they do a dummy standing in for a real response.  Its channels
are the dummy's, so a `chanlog` dummy gives the fake spectrum
logarithmically spaced channels.  The file
written carries no response, so reading it back needs a `dummyrsp` (or
a real response) again.

**Note For SPI/Integral Format:**

Since the SPI/Integral format builds its responses from a combination of 
multiple RMFs and ARFs, it must use a different scheme than the OGIP type I 
and II formats for storing RMF and ARF file location information.  This 
information is stored in a FITS extension, named ``RESPFILE_DB'' ,added to 
the PHA file.  Therefore, when fakeit prompts the user for the location of 
the response file, simply enter the name of a FITS file which contains a 
RESPFILE_DB extension pointing to the RMFs and ARFs to be applied.  When 
prompted for an ARF name, enter nothing.  

The prompts will only appear for the first spectrum in the data set, and 
the ARFs will be assigned row by row 1 to 1 with the spectra.   For example, 
if no data is currently loaded, to create 3 fake SPI spectra from the RMFs 
and ARFs named in the RESPFILE_DB extension of the file realSpiData.pha:

```
XSPEC> fakeit 3
// ...(various prompts will follow)...
For fake spectrum #1 response file is needed:  realSpiData.pha
// ...and ancillary file:  <Ret>
// ...(more fakeit prompts)...
```

This will create 3 fake spectra, each making use of the same RMFs/ARFs, 
spectrum 1 using the first row of the ARFs, spectrum 2 using the second etc.  

*** CAUTION - SPI/Integral ***

As currently implemented, the RESPFILE_DB method of storing ARF locations 
does not retain specific row information.  The assumption is that the rows 
in the ARF correspond 1 to 1 with the rows in the spectral data extension.  
Therefore, much confusion can arise when the row numbers of the loaded spectra 
do not match that of the fake spectra.   For example:

```
XSPEC> data my_spi_data.pha{3-4}
// my_spi_data.pha contains a RESPFILE_DB table pointing to
// arf1.fits, arf2.fits, arf3.fits.
// ...(fit to some model(s))...
XSPEC> fakeit 
```

This will produce 2 fake spectra generated from the model*response operation, 
where the model has parameters based on a fit to the original spectra in 
rows 3 and 4 of my_spi_data.pha, which used ROWS 3 AND 4 of the 3 arf 
files for their own responses.  However, the responses used above to generate 
the 2 fake spectra will use ROWS 1 AND 2 of the 3 arf files.  This is 
necessary since the fake spectra will be placed in rows 1 and 2 of their 
fakeit output file.

**Examples:**

**The keyword form:**

With nothing loaded, one spectrum through a real response and ARF, with a
background, 20 ks of exposure and a reproducible realization:

```
XSPEC> fakeit response=src.rmf arf=src.arf background=bkg.pha
         exposure=2e4 file=sim.fak seed=7
```

(all on one line).  This is the same as

```
XSPEC> xset seed 7
XSPEC> fakeit bkg.pha & src.rmf & src.arf & y & & sim.fak & 2e4
```

and writes sim.fak and sim_bkg.fak.

With two spectra loaded, one fake of each, at different exposures:

```
XSPEC> fakeit file=a.fak,b.fak exposure=1e4,5e4
```

With nothing loaded, three spectra on the dummy response, the response
written beside each, replacing any earlier run's files (on one line):

```
XSPEC> dummyrsp 0.3 10 500
XSPEC> fakeit writersp clobber file=d1.fak,d2.fak,d3.fak
         exposure=1000 3
```

Here `file=` is needed: the default names of new spectra on the same
response are all the same, and the keyword form refuses to write two spectra
to one file.

**Type I files:**

Using pre-loaded data:

For each of these examples, assume 3 spectra are currently loaded, each in 
its own type I file, and that the second spectrum has a background file. 

```
XSPEC> fakeit
```

This will produce 3 fake spectra each in its own type I output file, and 
the user will be prompted for the file names.  The response file information 
will come from each of the original spectra.  If any response information 
is invalid, the user will then be prompted.  A fake background file will 
be produced for the second spectrum.  

```
XSPEC> fakeit 4
```

Produces 4 fake spectra, the first 3 created as in the previous example.  
The fourth will be created with no background spectrum, and the user is 
prompted for response information.

```
XSPEC> fakeit backa,,none 4
```

Produces 4 fake spectra.  For the first spectrum, a fake background file 
will be generated from the file backa.  The second uses its own 
background file as before.  The third fake spectra will no longer use the 
response information from loaded spectrum 3, the user will be prompted instead, 
and its default numerical data will be reset to 1.  The fourth spectrum will 
be created as in the previous example.

Not using pre-loaded data:

If no data is currently loaded:  

```
XSPEC> fakeit 2
```

Produces 2 fake spectra in separate type I files, unless the user first 
entered response file belonging to a format that is explicitly type II (ie. 
SPI/Integral).

**Type II files:**

Using pre-loaded data:

Assume four spectra with no backgrounds have been loaded from one type II file:

```
XSPEC> data original_type2_data.pha{5-8}
```

Then, after model(s) have been entered and a fit:

```
XSPEC> fakeit 
```

This will produce 4 fake spectra in rows 1 to 4 of one type II output file, 
with responses and arfs taken from the columns of original_type2_data.pha.

```
XSPEC> fakeit ,,backb{1-3}
```

This produces 5 fake spectra in two type II output files, and 3 fake background 
spectra also placed in two type II output files:

The first 4 fake spectra are placed in one output file since that is how 
the 4 spectra they were based on were originally organized.  The default 
numerical data for this file are taken from the original spectra.  Fake 
spectra 3 and 4 now have backgrounds, based on `backb{1}` and 
`backb{2}` respectively.  These will generate 2 fake background 
spectra, placed in rows 3 and 4 of the first output fake background file.  
Rows 1 and 2 of this file will just consist of zeros since the first 2 
spectra have no backgrounds.
	
The fifth fake spectrum will be placed in the second type II PHA file.  
Response and numerical data will not be based on the existing loaded 
spectra.  A fake background will be generated from `backb{3}` and 
placed in row 1 of the second type II fake background file.

Not using pre-loaded data:

Now assume no data is currently loaded:

```
XSPEC> fakeit 2 backb{1}
```

2 fake spectra in one type II output file are produced, as is a 
corresponding fake background file with 2 rows.  The fact that the user 
has entered a type II background file on the command line tells fakeit to 
produce type II output.  The first fake spectrum will have no associated 
background, so row 1 in the fake background file will be all zeros.  
Row 2 will consist of the fake background generated from `backb{1}`.
