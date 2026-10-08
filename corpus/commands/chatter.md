---
name: chatter
aliases: [xchatter]
also_documents: []
source: XSchatter.tex
---

# chatter

**set verboseness level**

Control the verbosity of XSPEC.

**Syntax:** `chatter` <chatter level>  <log chatter>

where `<chatter level>` and `<log chatter>` are integer values.
`<chatter level>` applies to the terminal output and `<log chatter>`
to the log file (see `log`); each starts at 10.  Every message XSPEC
writes carries a level, and it is shown when its level is no higher than the
setting.  The levels form a ladder:

level & what it shows 

0  & nothing on the output stream (errors are always shown) 

5  & results: the fit result (principal axes, covariance, parameters,
     statistic), 

   & `error` results with their header, the grid of `steppar`, the
     output of 

   & commands that report (`show`, `flux`, `eqwidth`,
     ), and every warning 

10 & progress, the default: fit iterations, ``Reading '', notices on
     loading and 

   & grouping data, parameters pegging at a limit, model banners, sampler
     progress 

15 & diagnostics: fit-method trial information, input-file information,
     simulation detail 

20 & debugging: gradient dumps, chain trials, model internals 

25 & tracing of file reading and of the response; CFITSIO's own messages 

30 & internals: statistic terms, expression parsing, matrix dumps 

Each level includes everything below it.  Chatter 5 is the setting for
seeing a fit's answer without its iterations; values between the rungs
behave as the rung below them.  At 25 and above the terminal level also
switches on CFITSIO's verbose mode, which reports the FITS errors XSPEC
handles itself (an extension tried and not found, for instance).

Local models may write messages at any level they choose (see
Appendix AppendixAddModels); XSPEC's own are always one of the levels above.

**Examples:**

```
XSPEC> chatter 5
// Show fit results, error results and warnings, but not the fit's
// iterations.
XSPEC> chatter 10
// Set the terminal chattiness to 10, the initial value.
XSPEC> chatter ,0
// Set the chattiness for the log file to 0.
// This setting essentially disables the log file output.
XSPEC> chatter 10 25
// Restore the terminal chattiness to the initial level,
// while in the log file XSPEC will tell all
// (particularly when new data files are read in)
```
