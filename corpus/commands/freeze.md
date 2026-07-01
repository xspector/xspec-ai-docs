---
name: freeze
aliases: [rfreeze, xfreeze, xrfreeze]
also_documents: [rfreeze]
source: XSfreeze.tex
---

# freeze (and rfreeze)

**set parameters as fixed**

Do not allow indicated model parameters to vary. (See also `thaw`)

**Syntax:** `freeze` [<param range>...]

where `<param range>` ::= `[<modelName>:]<param#>|
<param#> - <param#>`.

**For response parameters** (see `gain` command):

**Syntax:** `rfreeze` [<param range>...]

where `<param range>` ::= `[<source number>:]<param#>|
<param#> - <param#>`.

The indicated model parameter or range of model parameters will be marked so 
they cannot be varied by the `fit` command. By default,the range will 
be the last range input by either a `freeze` or `thaw` command.

**Examples:**

Currently there are six parameters, initially all unfrozen.

```
XSPEC12> freeze 2 
//Parameter 2 is frozen
XSPEC12> freeze 4-6
//Parameters 4, 5, and 6 are frozen.
XSPEC12> thaw 2 3-5
//Parameters 2, 4, and 5 are thawed, parameter 3 is unaffected.
XSPEC12> freeze 
//Parameters 3,4,5 are frozen (the last range input by a freeze 
//or thaw command).
XSPEC12> rfreeze 4-6
//Response parameters 4, 5, and 6 are frozen.
```
