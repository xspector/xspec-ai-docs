---
name: rmodel
aliases: [xrmodel]
also_documents: [rmodelnone, rmodelclear]
source: XSrmodel.tex
---

# rmodel

**attach a response model to a detector response**

A **response model** transforms one detector response before the model
is folded through it: it may move the energy grid, change the effective
area, or change the matrix itself.  Response models are defined the way
model components are --- by an entry in `model.dat` of type
`rsp`, or in a local model package (see Appendix AppendixAddModels)
--- and are attached to a response by name with `rmodel`, which is to
responses what `model` is to sources.  Their parameters are
**response parameters**, edited with the **r**-prefixed commands
(`rnewpar`, `rfreeze`, `rthaw`, `runtie`,
`rerror`, `steppar` `r`$n$) and listed by
`show rpar`.

 p{} p{---6}}
**Syntax:** & **rmodel** & `[<sourceNum>:]<specNum> <name> [& <par1> & <par2> ...]`

 & **rmodel** & `[<sourceNum>:]<specNum> none [<name>]`

 & **rmodel** & `[<sourceNum>:]<specNum>`

 & **rmodel** & `clear`

 & **rmodel** & `?`

The first form attaches the response model `<name>` to the response
belonging to spectrum `<specNum>` (and source `<sourceNum>`, default
1).  The user is prompted for each of the model's parameters exactly as
`model` prompts for a component's, and the same answers may be given
after `&` delimiters on the command line; a bare `/` keeps a
parameter's default and `/*` keeps all the remaining ones.  The
parameters are created as variable fit parameters; freeze the ones that
are to stay fixed with `rfreeze`.  Attaching a name that is already
on the response replaces that model in place, keeping its position and its
parameter numbers; only the values supplied change.

`rmodel none` removes every response model from the named response,
or with a `<name>` just that one, and restores what the removed models
had transformed.  `rmodel clear` removes every response model from
every response.  With only the response address, `rmodel` lists the
models attached to that response, and `rmodel` `?` prints the
names of the response models available.

**The chain.**  A response may carry several response models.  They
are applied in succession, in the order they were attached, each to the
response as the previous ones left it; the order matters when the models do
not commute (a multiplicative correction evaluated on the energy grid after
a `gain` sees the shifted grid).  To change the order, remove and
re-attach.  Whenever any response parameter changes, the whole chain is
re-applied from the original response, so nothing accumulates from one
setting to the next.  Response parameters are numbered per source across
its responses in load order, then across each response's chain in attach
order, then in each model's own parameter order; `show rpar` lists
them with the model each belongs to.

**Built-in response models.**

- [gain] 

  The linear energy-scale shift of the `gain` command, with
  parameters `<slope>` and `<offset>` (keV).  Every edge of the
  energy grid on which the response is defined moves to
  $E' = E/\argdes{slope} - \argdes{offset}$ and the effective area is
  rebinned onto the moved grid; the matrix rows are unchanged.  The
  default hard limits (0.01--5 on the slope, $-1$--1 keV on the offset)
  are overridden by the GSLOP_MIN, GSLOP_MAX, GOFFS_MIN and GOFFS_MAX
  keywords when the matrix extension of the response file carries them.
  `gain` is a shorthand for attaching this model; see that command.

- [cgain] 

  The same idea in **channel** space: the matrix content of detector
  channel $c$ is moved to channel $c \times \argdes{slope} + \argdes{offset}$,
  with `<offset>` in channels.  An integer offset at slope 1 is an
  exact channel shift; a fractional one spreads each channel over the two
  it overlaps in proportion, and a slope other than 1 stretches the
  channel scale while conserving each energy row's total.  Content moved
  beyond either end of the channel range is lost.  The energy grid and the
  effective area are untouched; the matrix is regrouped to the spectrum's
  channels each time a parameter changes, which for a large matrix is a
  visible cost per fit iteration.

**Multiplicative models as response models.**  Any multiplicative
model component --- a built-in one, one defined with `mdefine`, or a
table with `mtable{<file>}` or `etable{<file>}`
--- may be attached with `rmodel`.  It is then evaluated on the
response's own energy grid (as left by the models before it in the chain)
and multiplied into the effective area, and its parameters become response
parameters.  The fit is the same as multiplying the source model by the
component, but the correction lives in the response: `flux`,
`lumin` and `eqwidth` report the source model without it, the
component is not evaluated on an `energies` extension, and a source
model shared by several spectra is still calculated once.  Additive,
convolution, pile-up and mixing components are refused.

**Local response models.**  A response model may be written as part
of a local model package with the `rsp` type and a C++ or C calling
sequence that receives working copies of the response matrix and effective
area; see Appendix AppendixAddModels.  `rmodel` `?` lists
them once the package is loaded.

**Restrictions.**  Response models are not supported on a dummy
response (`dummyrsp`, or a spectrum without a response).  On a
response built from several RMF files (`response` with more than one
matrix for one source), or from a file with several MATRIX extensions, the
chain is applied to every constituent matrix in turn, with the same
parameter values; a model that moves the energy grid must move every
constituent's grid alike.  A new `response` or `arf`
for a spectrum removes that response's models.  `ignore` and
`notice` do not affect them.

**Saving and reading back.**  `save all` writes each attached
model as an `rmodel` line followed by its parameter lines, in chain
order (the `mdefine` of a user-defined multiplicative model is written
ahead of the data it is attached to).  `tclout` `rmodel` returns
the names on a response's chain, `tclout` `rpar` a response
parameter's values, and `tclout` `gain` the two `gain`
parameters.

**Examples:**

```
XSPEC> rmodel 1 gain
// Attach the gain model to spectrum 1's response; prompts for the
// slope and offset, which become response parameters r1 and r2.
XSPEC> rmodel 2:1 cgain & 1.0 & 2.5
// A channel-space shift of 2.5 channels on source 2 of spectrum 1.
XSPEC> mdefine tilt exp(-a*(E-2)) : mul
XSPEC> rmodel 1 tilt & 0.1
// A user-defined multiplicative correction to spectrum 1's effective
// area, with its parameter a as a response parameter.
XSPEC> rmodel 1 mtable{corr.fits}
// A table model multiplied into the effective area; its table
// parameters are the response parameters.
XSPEC> rmodel 1
// List the models on spectrum 1's response in order of application.
XSPEC> rfreeze 3
XSPEC> rmodel 1 none tilt
// Freeze r3, then remove just the tilt model.
XSPEC> rmodel clear
// Remove every response model from every response.
```
