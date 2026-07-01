---
name: untie
aliases: [runtie, xruntie, xuntie]
also_documents: [runtie]
source: XSuntie.tex
---

# untie (and runtie)

**unlink previously linked parameters**

Untie the specified parameter from any links to other parameters.

**Syntax:** `untie` <param range>

where `<param range>` is of the form

`<param range>` ::= `[<modelName>:]<param #>`

For **response parameters** (see `gain` command):

 p{} l}
& **runtie** & `<param range>`

where `<param range>` is of the form

`<param range>` ::= `[<sourceNum>:]<param #>`

Parameters previously linked together with commands such as

`XSPEC12> newpar <param spec>`

are unlinked. The parameter will retain its current value for the next fit.
