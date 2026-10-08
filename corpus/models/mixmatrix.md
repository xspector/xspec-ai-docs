---
name: mixmatrix
type: mix  # mixing
func: U_MixMatrixModel
n_params: 0
family: [mixmatrix]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelMixmatrix.tex
---

# mixmatrix

**mixing model** (`mix`), function `U_MixMatrixModel`.

## Description

This is a general mixing model whose weights are supplied by the user
in a file, for when the way flux from one region reaches another is
known but no specific mixing model describes it. The mixed model
spectrum of a target region is
$$F'_t(E) = \sum_s w_{ts}(E)\, F_s(E)$$
where $F_s$ is the model spectrum of source region $s$ before mixing
and $w_{ts}$ the weight with which it reaches target $t$. A (target,
source) pair the file does not list contributes nothing --- including
the diagonal, so a region that keeps all its own flux needs an entry
of 1 for itself. The weights are either one number per pair or one per
energy bin.

Each spectrum takes part as the region given by an XFLTnnnn keyword
with the value ``MixRegion:N'', where N is an integer region number
(any numbering, as long as each spectrum's is unique). Spectra without
the keyword are left unmixed. The spectra may be in one data group or
several.

The weights file is named with

```
XSPEC> xset MIXMATRIX_FILE weights.fits
```

and is read when the model is calculated; setting a different file
takes effect at the next calculation. The file has a binary table
extension MIXMATRIX with one row per (target, source) pair and the
columns TARGET and SOURCE (region numbers, integer) and WEIGHT (double,
a scalar or a vector of one weight per energy bin). For
energy-dependent weights a second extension, MIXENERGIES, gives the
bins in the columns ENERG_LO and ENERG_HI: contiguous, increasing,
in keV or in any other energy or wavelength unit named by TUNITn. The
weights are interpolated onto each spectrum's model energies. Each pair
may appear only once; entries for regions with no spectrum loaded are
ignored. The heasp library (and its Python module) has a
`mixmatrix` class to write these files; the heasp guide gives
the format in full and an example.

The model is set to NaN, with a message saying why, when no file is
set, the file cannot be read or is inconsistent, or a loaded spectrum's
region does not appear in it; correcting the `xset` value
recovers it. Two spectra with the same MixRegion, or none with the
keyword, are refused when the model is defined.

For example, for three regions in which region 2's emission spills
into regions 1 and 3:

```
XFLT0001 = 'MixRegion:1'     (in region 1's spectrum, and similarly for 2 and 3)

XSPEC> data 1:1 reg1.pha 2:2 reg2.pha 3:3 reg3.pha
XSPEC> xset MIXMATRIX_FILE weights.fits
XSPEC> model mixmatrix(tbabs*apec)
```

`mixmatrix` has no parameters, so a fit's derivatives through
it are analytic wherever the rest of the model's are.
`tclout mixweights` lists the weights as the model applies them:
for energy-dependent weights, at a given energy.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|

## PyXspec

```python
from xspec import Model
m = Model("mixmatrix")
# component: m.mixmatrix  (params as attributes)
```
