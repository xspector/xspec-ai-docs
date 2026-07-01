---
name: compLS
type: add  # additive
func: compls
n_params: 3
family: [compLS]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCompls.tex
---

# compLS

**additive model** (`add`), function `compls`.

## Description

A Comptonization spectrum after [Lamb & Sanford (1979, MNRAS
288, 555)](https://ui.adsabs.harvard.edu/abs/1979MNRAS.188..555L/abstract). This model calculates the self-Comptonization of a
bremsstrahlung emission from an optically thick spherical plasma cloud
with a given optical depth and temperature. It was popular for Sco
X-1.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 2 | 0.01 | 10 | 0.001 | 20 | 0.001 |  |
| 2 | tau | — | 10 | 0.001 | 100 | 0.0001 | 200 | 0.0001 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("compLS")
# component: m.compls  (params as attributes)
```
