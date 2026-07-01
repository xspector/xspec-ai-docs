---
name: thaw
aliases: [rthaw, xrthaw, xthaw]
also_documents: [rthaw]
source: XSthaw.tex
---

# thaw (and rthaw)

**allow fixed parameters to vary**

Allow indicated parameters to vary. (See also `freeze`)

**Syntax:** `thaw` [<param range>...]

where `<param range>` ::= `[<modelName>:]<param#>|
<param#> - <param#>`.

**For response parameters** (see `gain` command):

**Syntax:** `rthaw` [<param range>...]

where `<param range>` ::= `[<source number>:]<param#>|
<param#> - <param#>`.

The indicated parameter, or range of parameters, will be marked as variable 
by the fitting commands and treated as a fitting parameter in subsequent 
fits. By default, the range will be the last range input by either a 
`freeze` or `thaw` command. See the `freeze` examples for an 
example of the use of the `thaw` command.
