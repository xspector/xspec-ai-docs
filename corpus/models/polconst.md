---
name: polconst
type: mul  # multiplicative
func: C_polconst
n_params: 2
family: [polconst]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPolconst.tex
---

# polconst

**multiplicative model** (`mul`), function `C_polconst`.

## Description

This multiplicative model applies a constant polarization. The factor
applied depends on which Stokes parameter the spectrum is for. The
Stokes parameter is determined using an
XFLTnnnn keyword with values ``Stokes:0'', ``Stokes:1'', or
``Stokes:2'', for I, Q, U, respectively.

Given the polarization fraction of A and the polarization angle in radians of psirad, 
then the multiplication factor is:
A*cos(2*psirad) for Q
A*sin(2*psirad) for U

The parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | A | — | 1 | 0 | 1 | 0 | 1 | 0.01 |  |
| 2 | psi | deg | 45 | -90 | 90 | -90 | 90 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("polconst*powerlaw")
# component: m.polconst  (params as attributes)
```
