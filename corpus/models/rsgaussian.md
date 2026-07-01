---
name: rsgaussian
type: add  # additive
func: C_rsgaussianLine
n_params: 4
family: [rsgauss]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRsgauss.tex
---

# rsgaussian

**additive model** (`add`), function `C_rsgaussianLine`.

## Description

A gaussian line profile with resonance scattering based on the optical
depth in the center of the line and the correction according to
[Chakraborty et al. (2023)](https://ui.adsabs.harvard.edu/abs/2023ApJ...959..126C/abstract). This
model is mainly for test purposes.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.5 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | keV | 0.1 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | Tau0 | — | 1 | 0 | 1000 | 0 | 1000 | 0.05 |  |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("rsgaussian")
# component: m.rsgaussian  (params as attributes)
```
