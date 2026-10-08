---
name: untie
aliases: [runtie, xruntie, xuntie]
also_documents: [runtie]
source: XSuntie.tex
---

# untie (and runtie, duntie)

**unlink previously linked parameters**

Untie the specified parameter from any links to other parameters.

**Syntax:** `untie` <param range>

**Syntax:** `untie` comp [<modelName>:]<c> [group <g>]

where `<param range>` is of the form

`<param range>` ::= `[<modelName>:]<param #>`

For **response parameters** (see the `rmodel` and `gain` commands):

 p{} l}
& **runtie** & `<param range>`

where `<param range>` is of the form

`<param range>` ::= `[<sourceNum>:]<param #>`

**For data parameters** (see the `dmodel` command), use `duntie` with data parameter numbers.

Parameters previously linked together with commands such as

`XSPEC> newpar <param spec>`

are unlinked. The parameter will retain its current value for the next fit.

`untie` `comp` unlinks every parameter of component <c>
(in data group <g>, the model's first if left out), keeping the values ---
the inverse of `newpar` `comp`.

One exception: a parameter of an ordinary mixing-model component (such as
`projct` or `xmmpsf`) belonging to a data group other than
the lowest cannot be made an independent fit parameter, because only the
lowest data group's copy of the component performs the transformation.
`untie` leaves such a parameter tied, with a message explaining why,
rather than creating a free parameter that no fit could move.
