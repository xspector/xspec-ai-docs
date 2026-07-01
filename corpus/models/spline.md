---
name: spline
type: mul  # multiplicative
func: xsspln
n_params: 6
family: [spline]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelSpline.tex
---

# spline

**multiplicative model** (`mul`), function `xsspln`.

## Description

A cubic spline modification.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Estart | keV | 0.1 | 0 | 100 | 0 | 100 | 0.05 |  |
| 2 | Ystart | — | 1 | -1000000 | 1000000 | -1000000 | 1000000 | 0.05 |  |
| 3 | Yend | — | 1 | -1000000 | 1000000 | -1000000 | 1000000 | 0.05 |  |
| 4 | YPstart | — | 0 | -1000000 | 1000000 | -1000000 | 1000000 | 0.05 |  |
| 5 | YPend | — | 0 | -1000000 | 1000000 | -1000000 | 1000000 | 0.05 |  |
| 6 | Eend | keV | 15 | 0 | 100 | 0 | 100 | 0.05 |  |

## PyXspec

```python
from xspec import Model
m = Model("spline*powerlaw")
# component: m.spline  (params as attributes)
```
