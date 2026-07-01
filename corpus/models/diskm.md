---
name: diskm
type: add  # additive
func: diskm
n_params: 5
family: [diskm]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelDiskm.tex
---

# diskm

**additive model** (`add`), function `diskm`.

## Description

A disk model with gas pressure viscosity. The spectrum from an
accretion disk where the viscosity scales as the gas pressure. From
[Stella and Rosner (1984)](https://ui.adsabs.harvard.edu/abs/1984ApJ...277..312S/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | accrate | — | 1 | 0.001 | 9 | 0.0001 | 10 | 0.01 |  |
| 2 | NSmass | Msun | 1.4 | 0.4 | 10 | 0.1 | 20 | 0.01 | frozen by default |
| 3 | Rinn | — | 1.03 | 1.01 | 1.03 | 1 | 1.04 | 0.001 | frozen by default |
| 4 | alpha | — | 1 | 0.01 | 10 | 0.001 | 20 | 0.001 | frozen by default |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("diskm")
# component: m.diskm  (params as attributes)
```
