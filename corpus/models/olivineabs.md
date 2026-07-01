---
name: olivineabs
type: mul  # multiplicative
func: F_olivineabs
n_params: 2
family: [olivineabs]
energy_range: [0.01, 1.e6]
source: manager/model.dat + XSmodelOlivineabs.tex
---

# olivineabs

**multiplicative model** (`mul`), function `F_olivineabs`.

## Description

A model for olivine absorption that uses the silicate absorption model
from `ismdust` incorporating the Fe Kedge from 
[Rogantini et al. (2018)](https://ui.adsabs.harvard.edu/abs/2018A%26A...609A..22R/abstract). Please
cite both 
[Corrales et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016MNRAS.458.1345C/abstract) and
[Rogantini et al. (2018)](https://ui.adsabs.harvard.edu/abs/2018A%26A...609A..22R/abstract) if you use this model.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | moliv | 10^-4 | 1 | 0 | 10000 | 0 | 100000 | 0.001 |  |
| 2 | redshift | — | 0 | 0 | 10 | -1 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("olivineabs*powerlaw")
# component: m.olivineabs  (params as attributes)
```
