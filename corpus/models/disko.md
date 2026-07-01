---
name: disko
type: add  # additive
func: disko
n_params: 5
family: [disko]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelDisko.tex
---

# disko

**additive model** (`add`), function `disko`.

## Description

A modified blackbody disk model. The spectrum from the inner region of
an accretion disk where the viscosity is dominated by radiation
pressure.

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
m = Model("disko")
# component: m.disko  (params as attributes)
```
