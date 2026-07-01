---
name: bvexpcheb6
type: add  # additive
func: C_bvexpcheb6
n_params: 25
family: [expcheb6, vexpcheb6, bexpcheb6, bvexpcheb6]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelExpcheb6.tex
---

# bvexpcheb6

**additive model** (`add`), function `C_bvexpcheb6`.

Variants documented together: `expcheb6`, `vexpcheb6`, `bexpcheb6`, `bvexpcheb6`.

## Description

`expcheb6` is a multi-temperature collisional-ionization
equilibrium model using the exponential of a sixth-order Chebyshev polynomial for the
differential emission measure. The switch parameter determines whether spectrum is
calculated by running the mekal code, by interpolating on a
pre-calculated mekal table, using the AtomDB data, or using the SPEX
data. The final two options
is now preferred. See the `cie` model for further information
and options. The reference for this model is [Singh et al. (1996,
ApJ, 456, 766)](https://ui.adsabs.harvard.edu/abs/1996ApJ...456..766S/abstract).

Velocity broadening can only be used with switch=2.

For `expcheb6` the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | CPcoef1 | — | 1 | -1 | 1 | -1 | 1 | 0.1 |  |
| 2 | CPcoef2 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 3 | CPcoef3 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 4 | CPcoef4 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 5 | CPcoef5 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 6 | CPcoef6 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 7 | nH | cm^-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 8 | He | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 9 | C | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 10 | N | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 11 | O | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 12 | Ne | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 13 | Na | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 14 | Mg | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 15 | Al | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 16 | Si | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 17 | S | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 18 | Ar | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 19 | Ca | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 20 | Fe | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 21 | Ni | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 22 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 23 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 24 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 25 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bvexpcheb6")
# component: m.bvexpcheb6  (params as attributes)
```
