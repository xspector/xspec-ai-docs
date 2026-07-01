---
name: pollin
type: mul  # multiplicative
func: C_pollin
n_params: 4
family: [pollin]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPollin.tex
---

# pollin

**multiplicative model** (`mul`), function `C_pollin`.

## Description

This multiplicative model applies a polarization with a linear
dependence on energy. The factor applied depends on which Stokes
parameter the spectrum is for. The Stokes parameter is determined
using an XFLTnnnn keyword with values ``Stokes:0'', ``Stokes:1'', or
``Stokes:2'', for I, Q, U, respectively.

The fraction and angle are determined by
$$A(E) = {\tt A1} + (E-1.0) \times {\tt Aslope}$$
$$\psi(E) = {\tt psi1} + (E-1.0) \times {\tt psislope}$$

The parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | A1 | — | 1 | 0 | 1 | 0 | 1 | 0.01 |  |
| 2 | Aslope | — | 0 | -5 | 5 | -5 | 5 | 0.01 |  |
| 3 | psi1 | deg | 45 | -90 | 90 | -90 | 90 | 0.01 |  |
| 4 | psislope | — | 0 | -5 | 5 | -5 | 5 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("pollin*powerlaw")
# component: m.pollin  (params as attributes)
```
