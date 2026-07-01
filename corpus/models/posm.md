---
name: posm
type: add  # additive
func: xsposm
n_params: 1
family: [posm]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelPosm.tex
---

# posm

**additive model** (`add`), function `xsposm`.

## Description

Positronium continuum ([Brown & Leventhal 1987](https://ui.adsabs.harvard.edu/abs/1987ApJ...319..637B/abstract))

A(E) = K{2(^2-9)E_c} [{E(E_c-E)(2E_c-E)^2}
 + {2E_c(E_c-E)E^2}\!({{E_c-E}E_c}) 

 {} - {2E_c(E_c-E)^2(2E_c-E)^3}\!({{E_c-E}E_c})
 + {(2E_c-E)E}]

for $E < E_c$ = 511 keV, where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("posm")
# component: m.posm  (params as attributes)
```
