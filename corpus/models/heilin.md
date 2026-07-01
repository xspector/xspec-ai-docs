---
name: heilin
type: mul  # multiplicative
func: xsphei
n_params: 3
family: [heilin]
energy_range: [0.01, 1.e20]
source: manager/model.dat + XSmodelHeilin.tex
---

# heilin

**multiplicative model** (`mul`), function `xsphei`.

## Description

This model calculates the Voigt absorption profiles for the He I series.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nHeI | 10^22 | 1e-05 | 0 | 1000000 | 0 | 1000000 | 1e-07 |  |
| 2 | b | km/s | 10 | 1 | 100000 | 1 | 1000000 | 1 |  |
| 3 | z | — | 0 | -0.001 | 100000 | -0.001 | 100000 | 1e-06 |  |

## PyXspec

```python
from xspec import Model
m = Model("heilin*powerlaw")
# component: m.heilin  (params as attributes)
```
