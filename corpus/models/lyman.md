---
name: lyman
type: mul  # multiplicative
func: xslyman
n_params: 4
family: [lyman]
energy_range: [0.01, 1.e20]
source: manager/model.dat + XSmodelLyman.tex
---

# lyman

**multiplicative model** (`mul`), function `xslyman`.

## Description

This model calculates the Voigt absorption profiles for the H I and He II Lyman series.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | n | 10^22 | 1e-05 | 0 | 1000000 | 0 | 1000000 | 1e-07 |  |
| 2 | b | km/s | 10 | 1 | 100000 | 1 | 1000000 | 1 |  |
| 3 | z | — | 0 | -0.001 | 100000 | -0.001 | 100000 | 1e-06 |  |
| 4 | ZA | — | 1 | 1 | 2 | 1 | 2 | 0.1 |  |

## PyXspec

```python
from xspec import Model
m = Model("lyman*powerlaw")
# component: m.lyman  (params as attributes)
```
