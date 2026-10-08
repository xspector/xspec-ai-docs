---
name: show
aliases: [xshow]
also_documents: [showabund, showall, showallfile, showcontrol, showdata, showfree, showfrozen, showfiles, showfit, showlinked, showmodel, shownoticed, showparameters, showpar, showdparameters, showdpar, showpha, showplot, showrates, showresponse, showrparameters, showrpar, showversion, showxsect]
source: XSshow.tex
---

# show

**output current program state**

List selected information to the user's terminal (and the log file, if open).

**Syntax:** `show` [<selection>]

where `<selection>` is a key word to select the information to 
be printed. If omitted, it is the information last asked for. 
Initially, the default selection is `all`.  (Note: to better 
integrate the usage of OGIP type-II files, much of the information 
given by `show files` in previous versions is now displayed by 
`show data`.)

Selections are:

- [`abund`]Show current solar abundance table.

- [`all`]All the information.

- [`allfile`]All file information = files + noticed + rates.

- [`control`]XSPEC control information:
  auto-saving, fit querying, renorming and the default systematic error,
  then the settings `xset` changes, as a bare `xset` lists them
  (fit and test statistic, weighting, fit method, chain rule, abundance and
  cross-section tables, cosmology, model data directory and random-number
  seed).

- [`data`]File names, associated
  coefficients, and net countrates, displayed in order of spectrum
  number.  For higher chatter, also displays grouping map.

- [`free`]Like `parameters` but
  only shows free parameters, and likewise followed by the fit statistic.

- [`frozen`]Like `parameters`
  but only shows frozen parameters.

- [`files`]Equivalent to 
  `show data` but displayed in order of file name, and with the
  extension each file was read from: after the spectrum, background,
  correction, response and ARF file names, in parentheses, the extension
  name and its HDU number (counting the primary array as 0, as
  `file[n]` does), and for a type II file the row, e.g.\
  `(SPECTRUM, HDU 2, row 3)`.  A response lists the MATRIX
  extension it uses -- each of them, for a multi-binning response -- then the
  EBOUNDS.

- [`fit`]Fit information.

- [`linked`,`tied`]Like
  `parameters` but only shows linked parameters.

- [`model`]The model specification.

- [`noticed`]Channel ranges noticed for each file.

- [`parameters`]All current
  parameter values (including gain parameters, if any). Adding
  `<[name:]par range>` shows the subset of all model parameters
  given by `<[name:]par range>` where name is the model name if
  named models are in use, e.g. **show parameters 1,3,5-8** or
  **show parameters mymodel:1-4**. Adding instead `<comp
    [name:]range>` shows all model parameters in the requested
  component numbers while `<group [name:]range>` does the same
  thing for the requested data group numbers.  The parameters are followed by
  the fit statistic, as `show fit` prints it.

- [`dparameters`]All current
  data parameters (those of the data models attached with `dmodel`),
  with the spectrum and model each belongs to, followed by the fit statistic.

- [`pha`]Current data, error and model values for each channe.

- [`plot`]Current plot settings from setplot command, include rebinning info.

- [`rates`]Folded model, correction rates for each file.

- [`response`]Show responses loaded, with
  the response models attached to each and their parameter values.

- [`rparameters`]All current
  response parameters (those of the `gain` and other response models
  attached with `rmodel`), with the model each belongs to. Adding
  `<par range>` shows the subset of all response parameters given by
  `<par range>`.  Followed by the fit statistic, as for
  `parameters`.

- [`version`]Show the XSPEC version number.

- [`xsect`]Show description of cross-section table
