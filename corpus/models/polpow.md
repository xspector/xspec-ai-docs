---
name: polpow
type: mul  # multiplicative
func: C_polpow
n_params: 4
family: [polpow]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPolpow.tex
---

# polpow

**multiplicative model** (`mul`), function `C_polpow`.

## Description

This multiplicative model applies a polarization with a power-law
dependence on energy. The factor applied depends on which Stokes
parameter the spectrum is for. The Stokes parameter is determined
using an XFLTnnnn keyword with values ``Stokes:0'', ``Stokes:1'', or
``Stokes:2'', for I, Q, U, respectively.

The fraction and angle are determined by
$$A(E) = {\tt Anorm} \times E^{-{\tt Aindex}}$$
$$\psi(E) = {\tt psinorm} \times E^{-{\tt psiindex}}$$

The parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Anorm | — | 1 | 0 | 1 | 0 | 1 | 0.01 |  |
| 2 | Aindex | — | 0 | -5 | 5 | -5 | 5 | 0.01 |  |
| 3 | psinorm | deg | 45 | -90 | 90 | -90 | 90 | 0.01 |  |
| 4 | psiindex | — | 0 | -5 | 5 | -5 | 5 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("polpow*powerlaw")
# component: m.polpow  (params as attributes)
```
