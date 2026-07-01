---
name: zbbody
type: add  # additive
func: xszbod
n_params: 3
family: [bbody, zbbody]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelBbody.tex
---

# zbbody

**additive model** (`add`), function `xszbod`.

Variants documented together: `bbody`, `zbbody`.

## Description

A blackbody spectrum. 

$$A(E) = {{K \times 8.0525 E^2 dE}\over{(kT)^4[\exp(E/kT)-1]}}$$

where

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 3 | 0.01 | 100 | 0.0001 | 200 | 0.01 |  |
| 2 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zbbody")
# component: m.zbbody  (params as attributes)
```
