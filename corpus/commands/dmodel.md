---
name: dmodel
aliases: [xdmodel]
also_documents: [dmodelnone, dmodelclear, dnewpar, dfreeze, dthaw, duntie]
source: XSdmodel.tex
---

# dmodel (and dnewpar, dfreeze, dthaw, duntie)

**attach a data model to a spectrum**

A **data model** changes one of the scales with which a spectrum's
data enter the fit statistic, and nothing else: the correction-file scale
$c$ (the `cornorm` of the spectrum) or a factor $b$ on the background
scale $\alpha$, so that the background enters as $b\alpha B$.  It never
touches the source model or the response.  Data models are defined the way
model components are --- by an entry in `model.dat` of type
`dat`, or in a local model package (see
Appendix AppendixAddModels) --- and are attached to a spectrum by name
with `dmodel`, which is to spectra what `rmodel` is to
responses.  Their parameters are **data parameters**, numbered
$d1, d2, \ldots$ across every spectrum, and edited with the
**d**-prefixed commands (`dnewpar`, `dfreeze`,
`dthaw`, `duntie`, `derror`, `steppar` `d`$n$,
`bayes` `d`$n$) and listed by `show dparameters`.

 p{} p{---6}}
**Syntax:** & **dmodel** & `<specNum> <name> [& <par1> & <par2> ...]`

 & **dmodel** & `<specNum> none [<name>]`

 & **dmodel** & `<specNum>`

 & **dmodel** & `clear`

 & **dmodel** & `?`

The first form attaches the data model `<name>` to spectrum
`<specNum>`.  The user is prompted for each of its parameters as
`model` prompts for a component's, and the answers may be given after
`&` delimiters instead.  Attaching a name already on the spectrum
replaces only the values supplied.  `dmodel none` removes the
spectrum's data models, or with a `<name>` just that one, and the
spectrum's scales return to their nominal values (the CORRSCAL or
`cornorm`, and $b=1$).  `dmodel clear` removes every data
model from every spectrum.  With only the spectrum number, `dmodel`
lists the models on it with their data parameters, and
`dmodel` `?` prints the names of the data models available.

**Rules.**  A spectrum carries at most one data model per scale: a
second model setting the correction scale (or the background factor) is
refused until the first is removed, since the later would silently undo
the earlier.  A model is refused if the spectrum lacks the quantity it
sets --- `recorn` without a correction file (`corfile`),
`bkgnorm` without a background (`backgrnd`; a background
taken over by `backmodel` counts as none).  If the correction file or
background is removed after the model is attached, the model stays but is
inactive, and its parameters are not fit variables until the quantity
returns.

**Data parameters.**  The commands for them take data parameter
numbers and behave as their model-parameter counterparts do:

 p{} l}
**Syntax:** & **dnewpar** & `<n> [<value> [<delta> <min> <bot> <top> <max>]]`

 & **dnewpar** & `<n> = <expression of d parameters>`

 & **dfreeze** & `<n1>[-<m1>] ...`

 & **dthaw** & `<n1>[-<m1>] ...`

 & **duntie** & `<n1>[-<m1>] ...`

A data parameter may be linked only to other data parameters
(`dnewpar 2 = d1`).  `derror` takes the arguments of
`error` with data parameter numbers; `steppar` steps one as
`d`$n$, and `bayes` `d`$n$ sets its prior (used once `bayes on`).  Fits
differentiate through a data parameter by the chain rule: the derivative of
the statistic with respect to the scale (analytic for $c$; for $b$ a
central difference of the statistic, with no model evaluation) times the
derivative of the scale with respect to the parameter, which the data model
supplies (or which is differenced numerically for a local model that does
not).

**Built-in data models.**

- [recorn] 

  The correction-file scale: its one parameter, `<Cornorm>`, replaces
  the spectrum's CORRSCAL or `cornorm` while attached, and is free by
  default.  It starts at 1 unless a value is given.  See
  `recorn` in Chapter Models.

- [bkgnorm] 

  A factor `<Bnorm>` $=b$ on the background scale, $\alpha \to
  b\alpha$, under every statistic: the subtracted background and its
  variance for $\chi^2$, the profiled background of W and pgstat.  It is
  frozen at 1 by default; thaw it to fit the background normalization, and
  constrain it with a prior (`bayes` `d`$n$), since the source
  and background normalizations are otherwise nearly degenerate.  See
  `bkgnorm` in Chapter Models.

**The old recorn.**  `recorn` used to be a mixing model,
written first in a model expression with a spectrum number and a cornorm
per data group.  That form is still read: `model`, `editmod`
and `addcomp` take `recorn` out of the expression and attach
it to the spectrum it named with `dmodel`, reporting each move and,
once per session, that the form is deprecated; it will be removed in a
later release.  Scripts can be converted with
`xsmigrate_local_model --xcm` (Appendix AppendixAddModels).

**Simulations.**  `fakeit`, `goodness`, `sim`,
`lrt` and `coverage` simulate with the scales in force --- the
correction as $c$ times the correction file and the background as
$b\alpha B$ --- and draw free data parameters with the others.  A file
written by `fakeit` carries the nominal CORRSCAL and BACKSCAL, so a
data model is not applied twice when it is read back; the data models are
re-attached to the fake spectra.

**Saving and reading back.**  `save all` writes each data
model as a `dmodel` line with its parameter settings, and links as
`dnewpar` lines after them.  `tclout` `dmodel`
returns the names on a spectrum, `tclout` `dpar` a data
parameter's values and `tclout` `derror` its last error.  A new
`data` for a spectrum removes its data models.
`bias` refuses a fit with free data parameters.

**Examples:**

```
XSPEC> data 1:1 src1.pha 2:2 src2.pha
XSPEC> corfile 1 corr1.pha
XSPEC> dmodel 1 recorn & 0.8
// Fit spectrum 1's correction norm, starting at 0.8; it is d1.
XSPEC> dmodel 2 bkgnorm
XSPEC> dthaw 2
XSPEC> bayes d2 lognormal 1 0.1
XSPEC> bayes on
// Fit a factor on spectrum 2's background scaling, with a 10 per cent
// lognormal prior.
XSPEC> show dpar
XSPEC> derror 1
XSPEC> dmodel 2 none
// Remove spectrum 2's data models: its background scale is nominal again.
```
