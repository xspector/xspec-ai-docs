---
name: bbodyrad
type: add  # additive
func: xsbbrd
n_params: 2
family: [bbodyrad]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelBbodyrad.tex
---

# bbodyrad

**additive model** (`add`), function `xsbbrd`.

## Description

A blackbody spectrum with normalization proportional to the surface area.

$$A(E) = {{K \times 1.0344 \times 10^{-3} E^2 dE}\over{\exp(E/kT)-1}}$$

where

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 3 | 0.001 | 100 | 0.0001 | 200 | 0.01 |  |
| 2 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bbodyrad")
# component: m.bbodyrad  (params as attributes)
```
