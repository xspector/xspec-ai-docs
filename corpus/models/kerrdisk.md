---
name: kerrdisk
type: add  # additive
func: dospin
n_params: 10
family: [kerrdisk]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelKerrdisk.tex
---

# kerrdisk

**additive model** (`add`), function `dospin`.

## Description

Model for an accretion disk broad emission line with the black hole
spin allowed to be a free parameter. A detailed description can be
found in [Brenneman & Reynolds (2006)](https://ui.adsabs.harvard.edu/abs/2006ApJ...652.1028B/abstract).

This model is quite slow so is best used after models such as `laor` or
`diskline` have been employed to get an estimate of the best-fit
parameters.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | lineE | keV | 6.4 | 0.1 | 100 | 0.1 | 100 | 0.1 | frozen by default |
| 2 | Index1 | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 3 | Index2 | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 4 | r_br_g | — | 6 | 1 | 400 | 1 | 400 | 0.1 | frozen by default |
| 5 | a | — | 0.998 | 0.01 | 0.998 | 0.01 | 0.998 | 0.1 |  |
| 6 | Incl | deg | 30 | 0 | 90 | 0 | 90 | 1 | frozen by default |
| 7 | Rin_ms | — | 1 | 1 | 400 | 1 | 400 | 0.1 | frozen by default |
| 8 | Rout_ms | — | 400 | 1 | 400 | 1 | 400 | 0.1 | frozen by default |
| 9 | z | — | 0 | 0 | 10 | 0 | 10 | 0.001 | frozen by default |
| 10 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("kerrdisk")
# component: m.kerrdisk  (params as attributes)
```
