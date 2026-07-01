---
name: swind1
type: mul  # multiplicative
func: C_swind1
n_params: 4
family: [swind1]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelSwind1.tex
---

# swind1

**multiplicative model** (`mul`), function `C_swind1`.

## Description

A model to fit the soft excess in AGN by partially ionized absorbing material 
with large velocity shear. It approximates this by using XSTAR kn5 
photoionization absorption model grids (calculated assuming a microturbulent 
velocity of 100km/s), and then convolving this with Gaussian smearing. 
This is the model used by [Gierlinski & Done (2006)](https://ui.adsabs.harvard.edu/abs/2006MNRAS.371L..16G/abstract), [Sobolewska & Done (2007)](https://ui.adsabs.harvard.edu/abs/2007MNRAS.374..150S/abstract) 
and Done et al (2006). It is an update (uses a newer version of XSTAR) of the 
original model of [Gierlinski & Done (2004)](https://ui.adsabs.harvard.edu/abs/2004MNRAS.347..885G/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | column | — | 6 | 3 | 50 | 3 | 50 | 0.01 |  |
| 2 | log_xi | — | 2.5 | 2.1 | 4.1 | 2.1 | 4.1 | 0.01 |  |
| 3 | sigma | — | 0.1 | 0 | 0.5 | 0 | 0.5 | 0.01 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("swind1*powerlaw")
# component: m.swind1  (params as attributes)
```
