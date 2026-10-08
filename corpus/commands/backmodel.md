---
name: backmodel
aliases: [xbackmodel]
also_documents: []
source: XSbackmodel.tex
---

# backmodel

**fit the background with a model, together with the source**

Set up the simultaneous fit of a source spectrum and its background, with
the background described by a model rather than subtracted (or profiled, as
the W-statistic does).  This automates the recipe described in the
*Poisson data with Poisson background* section of
Appendix AppendixStatistics.

 p{} p{---6}}
**Syntax:** & **backmodel** & `[`<name>`:] [`<spectra>`] `<model expression>` [response=`<file>`|diagonal] [arf=`<file>`|none]`

                 & **backmodel** & `none [`<spectra>`]`

                 & **backmodel** &

where `<name>` is the name of this background component (default
`bkg`), `<spectra>` a list of source spectrum numbers and ranges
such as `1,3-4` (default: every loaded spectrum with a background
file), and `<model expression>` any expression the `model`
command accepts.

For each of those spectra:

- The background file is loaded as a spectrum of its own, numbered after
  the spectra already loaded, in the *same* data group as its source
  spectrum.  The source spectrum stops using that background file -- it is
  neither subtracted nor profiled -- and the file is remembered so that
  `backmodel none` can put it back.

- The model becomes a named model, `<name>`, on a source number of
  its own.  On the background spectrum it is folded through, in order of
  preference, the `response=` and `arf=` files, the background
  file's own RESPFILE and ANCRFILE, or the source spectrum's RMF with no ARF
  (XSPEC says so when it takes this last choice).

- On the source spectrum it is folded through the source spectrum's own
  RMF and ARF -- a sky component inside the source region is vignetted like
  the source -- and multiplied channel by channel by the ratio of the
  extraction areas, $r_i = $ BACKSCAL$_{\rm src}/$BACKSCAL$_{\rm bkg}$ (a
  BACKSCAL column gives a different $r_i$ in each channel).  AREASCAL needs
  no factor: each spectrum's fold already includes its own, which together
  reproduce the scaling background subtraction uses.  `show response`
  lists the multiplier.

- Every other model source has no response on the background spectrum,
  so the source models do not contribute to it.

- The background model's parameters are *not* linked across data
  groups (the backgrounds of two instruments usually differ), unlike those of
  a model defined with `model`.  Its parameters start at their
  defaults; set them with `newpar` `<name>`:`<n>`.

Several components can share the background spectra -- for instance a sky
component through the ARF and an instrumental (particle) component without
one:

```
XSPEC> backmodel sky: apec + powerlaw
XSPEC> backmodel nxb: constant*bknpower arf=none
```

`arf=none` also drops the source ARF on the source spectrum, and
`response=diagonal` folds the component through a diagonal response on
both spectra.  Issuing `backmodel` again with the name of an existing
component replaces it.  Cross-normalisation between the source and
background regions is not built in: add a `constant` to the
expression if it is wanted.

Once set up, the background spectra are ordinary spectra: `show`,
`plot`, `tclout`, `ignore`/`notice` and
`response`/`arf` all act on them.  A background spectrum starts
with the noticed channels of its source spectrum and is independent
afterwards, so more background channels can be noticed to constrain the
model.  The statistic of each source spectrum is computed without a
background: `cstat` there is the plain C-statistic rather than the
W-statistic (XSPEC notes this once).

`backmodel none` undoes the set-up for the listed source spectra (all
of them by default): the background spectra are deleted, each source
spectrum gets its background file back, and a component that no longer
covers any spectrum is deleted with its model.  `backmodel` with no
arguments lists the components and the managed spectra.

While a spectrum is managed by `backmodel`:

- `backgrnd` on the source or background spectrum, and `data`
  replacing or deleting a background spectrum, are refused;
  `backmodel none` comes first.

- Deleting a source spectrum deletes its background spectrum.
  Replacing it (`data` `1 new.pha`) loads the new file's
  background in the same way, for the same components; a file without one
  is dropped from the set-up with a note.

- `fakeit` simulates the source spectrum including the background
  model's contribution, and the background spectrum from the background
  model; no background file is written.

- `save` writes the `backmodel` commands and the background
  models' parameters, not the expanded spectra and responses; on replay the
  background spectra come back after all the others.

**Examples:**

```
XSPEC> data 1:1 src.pha
XSPEC> model phabs(apec)
XSPEC> backmodel powerlaw
// src.pha's BACKFILE becomes spectrum 2, in data group 1; the model
// "bkg" (powerlaw) is folded through the background file's own
// response on spectrum 2, and through src.pha's response times
// BACKSCAL(src)/BACKSCAL(bkg) on spectrum 1.
XSPEC> backmodel nxb: 1 constant*powerlaw arf=none
// An unfocused instrumental component on the same background spectrum.
XSPEC> backmodel none
// Back to subtracting the background file from spectrum 1.
```
