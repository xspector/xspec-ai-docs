---
name: cornorm
aliases: [xcornorm]
also_documents: []
source: XScornorm.tex
---

# cornorm

**change the normalization of the correction file**

Reset the normalization used in correcting the background.

**Syntax:** `cornorm` [[<spectrum range>...] [<cornorm>]]...

where `<spectrum range>` ::=  `<first spectrum no.>` - `<last spectrum no.>` 
is a range of spectra to which the correction is to be applied and  `<cornorm>` is the 
value to be used for the normalization. A decimal point (.) is used to 
distinguish a correction norm from a single spectrum `<spectrum range>`. 
If no correction norm is given, then the last value input is used (the initial 
value is one (1)). If no range is given, then the last single range input is 
modified. (See the `corfile` command.) 

**Examples:**
  
Assume that there are four spectra, all with associated correction files already 
defined, either by default in their PHA file, or explicitly by using the 
`corfile` command.

```
XSPEC12> cornorm 1-4 1.
//The correction norm for all four is set to 1.0
XSPEC12> cornorm 0. 1-2 0.3 
//The correction norm for the last input range (which was 1-4) 
// is set to 0., then files 1 and 2 are reset to 0.3.
XSPEC12> cornorm 4
//file 4 has the correction also set to 0.3.
XSPEC12> cornorm 1 4 -.3
//files 1 and 4 are set to -.3.
XSPEC12> cornorm .7
//file 4 (as the last input single range) is set to 0.7.
```
