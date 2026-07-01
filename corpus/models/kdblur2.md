---
name: kdblur2
type: con  # convolution
func: C_kdblur2
n_params: 6
family: [kdblur2]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelKdblur2.tex
---

# kdblur2

**convolution model** (`con`), function `C_kdblur2`.

## Description

A convolution model to smooth a spectrum by relativistic effects from an 
accretion disk around a rotating black hole. The accretion disk has a 
broken-power law emissivity profile. Uses Ari Laor's calculation 
including GR effects ([Laor 1991](https://ui.adsabs.harvard.edu/abs/1991ApJ...376...90L/abstract)). Modified from `laor2` model by 
Andy Fabian and Roderick Johnstone.

Note that due to the energy binning the convolution process can
produce spurious structures around sharp features in the spectrum
being convolved. We strongly recommend testing for this by using the
`energies` command to change the binning.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Index | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 2 | Rin_G | — | 4.5 | 1.235 | 400 | 1.235 | 400 | 0.1 | frozen by default |
| 3 | Rout_G | — | 100 | 1.235 | 400 | 1.235 | 400 | 0.1 | frozen by default |
| 4 | Incl | deg | 30 | 0 | 90 | 0 | 90 | 1 |  |
| 5 | Rbreak | — | 20 | 1.235 | 400 | 1.235 | 400 | 0.1 | frozen by default |
| 6 | Index1 | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("kdblur2*powerlaw")
# component: m.kdblur2  (params as attributes)
```
