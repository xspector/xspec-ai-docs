---
name: laor2
type: add  # additive
func: C_laor2
n_params: 8
family: [laor2]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLaor2.tex
---

# laor2

**additive model** (`add`), function `C_laor2`.

## Description

An emission line from an accreti on disk with a broken power-law
emissivity profile around a black hole. Uses Ari Laor's calculation
including GR effects ([Laor (1991)](https://ui.adsabs.harvard.edu/abs/1991ApJ...376...90L/abstract)). Modified from laor model by Andy
Fabian.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | lineE | keV | 6.4 | 0 | 100 | 0 | 100 | 0.05 |  |
| 2 | Index | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 3 | Rin_G | — | 1.235 | 1.235 | 400 | 1.235 | 400 | 0.1 | frozen by default |
| 4 | Rout_G | — | 400 | 1.235 | 400 | 1.235 | 400 | 0.1 | frozen by default |
| 5 | Incl | deg | 30 | 0 | 90 | 0 | 90 | 1 | frozen by default |
| 6 | Rbreak | — | 20 | 1.235 | 400 | 1.235 | 400 | 0.1 | frozen by default |
| 7 | Index1 | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 8 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("laor2")
# component: m.laor2  (params as attributes)
```
