---
name: compST
type: add  # additive
func: compst
n_params: 3
family: [compST]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCompst.tex
---

# compST

**additive model** (`add`), function `compst`.

## Description

A Comptonization spectrum after [Sunyaev & Titarchuk (1980, A&A 86,
121)](https://ui.adsabs.harvard.edu/abs/1980A&A....86..121S/abstract). This model is the Comptonization of cool photons on hot
electrons.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 2 | 0.01 | 100 | 0.001 | 100 | 0.001 |  |
| 2 | tau | — | 10 | 0.001 | 100 | 0.0001 | 200 | 0.0001 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("compST")
# component: m.compst  (params as attributes)
```
