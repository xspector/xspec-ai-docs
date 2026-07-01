---
name: zvfeabs
type: mul  # multiplicative
func: xszvfe
n_params: 5
family: [zvfeabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelZvfeabs.tex
---

# zvfeabs

**multiplicative model** (`mul`), function `xszvfe`.

## Description

Redshifted photoelectric absorption with all abundances tied to Solar except 
for iron. The Fe K edge energy is a free parameter.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | metals | — | 1 | 0 | 100 | 0 | 100 | 0.1 |  |
| 3 | FEabun | — | 1 | 0 | 100 | 0 | 100 | 0.1 |  |
| 4 | FEKedge | keV | 7.11 | 7 | 9.5 | 7 | 9.5 | 0.1 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zvfeabs*powerlaw")
# component: m.zvfeabs  (params as attributes)
```
