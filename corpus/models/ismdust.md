---
name: ismdust
type: mul  # multiplicative
func: F_ismdust
n_params: 3
family: [ismdust]
energy_range: [0.01, 1.e6]
source: manager/model.dat + XSmodelIsmdust.tex
---

# ismdust

**multiplicative model** (`mul`), function `F_ismdust`.

## Description

This model provides the extinction (= absorption + scattering) properties for 
a power law distribution of dust grains using the optical properties
for dust provided in [Draine (2003)](https://ui.adsabs.harvard.edu/abs/2003ApJ...598.1026D/abstract). The
default mixture of 60% / 40% silicate / graphite is described in
[Corrales et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016MNRAS.458.1345C/abstract).
Please cite this paper if you use this model.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | msil | 10^-4 | 1 | 0 | 10000 | 0 | 100000 | 0.001 |  |
| 2 | mgra | 10^-4 | 1 | 0 | 10000 | 0 | 100000 | 0.001 |  |
| 3 | redshift | — | 0 | 0 | 10 | -1 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("ismdust*powerlaw")
# component: m.ismdust  (params as attributes)
```
