---
name: recorn
type: dat  # dat
func: C_recorn
n_params: 1
family: [recorn]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRecorn.tex
---

# recorn

**dat model** (`dat`), function `C_recorn`.

## Description

A data model (attached with `dmodel`, not written in a model
expression) whose one parameter is the scale $c$ of the spectrum's
correction file: while it is attached, the correction subtracted from the
data is $c$ times the correction file, in place of the CORRSCAL or
`cornorm` value, and $c$ can be fitted.  This replaces and improves
on the old command `recornrm`.

```
XSPEC>corfile 1 corr.pha
XSPEC>dmodel 1 recorn & 0.8
```

The parameter starts at 1 unless a value is given; give the spectrum's
current `cornorm` to start the fit from it.  The fit differentiates
the statistic with respect to $c$ analytically.  `recorn` is
refused on a spectrum without a correction file, and a spectrum carries at
most one data model setting its correction scale.  To fit the correction
norms of several spectra, attach a `recorn` to each: they are
independent data parameters, whatever the data groups.  When the model is
removed (`dmodel none`) the correction returns to the nominal
`cornorm`.  Simulations (`fakeit`, `sim`,
`goodness`) use the fitted $c$, and `fakeit` writes the nominal
CORRSCAL to its files.

**The old form.**  `recorn` used to be a mixing model, written
first in a model expression with a spectrum number and a cornorm in each
data group, as in `model recorn*phabs*powerlaw`.  That form is
deprecated, and will be removed in a later release, but is still read: the
component is taken out of the expression and each data group's copy
attached, as `dmodel <spectrum> recorn & <cornorm>`, to
the spectrum its first parameter named (the last copy naming a spectrum
wins).  XSPEC reports each move and says once per session that the form is
deprecated.  `xsmigrate_local_model --xcm` rewrites a script or
save file in the new form (Appendix AppendixAddModels).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Cornorm | — | 1 | -10 | 10 | -10 | 10 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("recorn")
# component: m.recorn  (params as attributes)
```
