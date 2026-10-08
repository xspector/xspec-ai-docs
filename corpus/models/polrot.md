---
name: polrot
type: mix  # mixing
func: U_RotatePolarization
n_params: 1
family: [polrot]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPolrot.tex
---

# polrot

**mixing model** (`mix`), function `U_RotatePolarization`.

## Description

This mixing model rotates the polarization assuming at least two spectra, for
the Q and U Stokes parameters.
$$Q_{new} = Q\times cos(2\theta) - U\times sin(2\theta)$$
$$U_{new} = Q\times sin(2\theta) + U\times cos(2\theta)$$

Which spectrum is from which Stokes parameter is determined using an
XFLTnnnn keyword with values ``Stokes:0'', ``Stokes:1'', or
``Stokes:2'', for I, Q, U, respectively.

Any spectra other than Q or U included in the fit will be
unchanged. Any datagroup containing one of Q or U must contain the
other and there should only be one pair of Q and U per datagroup.

The parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Angle | deg | 0 | -180 | 180 | -180 | 180 | 0.1 |  |

## PyXspec

```python
from xspec import Model
m = Model("polrot")
# component: m.polrot  (params as attributes)
```
