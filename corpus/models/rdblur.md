---
name: rdblur
type: con  # convolution
func: C_rdblur
n_params: 4
family: [rdblur]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRdblur.tex
---

# rdblur

**convolution model** (`con`), function `C_rdblur`.

## Description

A convolution model to smooth a spectrum by relativistic effects from an 
accretion disk around a non-rotating black hole. Modified from `diskline` 
model ([Fabian et al. (1989)](https://ui.adsabs.harvard.edu/abs/1989MNRAS.238..729F/abstract)) by Andy Fabian and Roderick Johnstone.

Note that due to the energy binning the convolution process can
produce spurious structures around sharp features in the spectrum
being convolved. We strongly recommend testing for this by using the
`energies` command to change the binning.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Betor10 | — | -2 | -10 | 20 | -10 | 20 | 0.01 | frozen by default |
| 2 | Rin_M | — | 10 | 6 | 1000 | 6 | 10000 | 0.1 | frozen by default |
| 3 | Rout_M | — | 1000 | 0 | 1000000 | 0 | 10000000 | 1 | frozen by default |
| 4 | Incl | deg | 30 | 0 | 90 | 0 | 90 | 0.05 |  |

## PyXspec

```python
from xspec import Model
m = Model("rdblur*powerlaw")
# component: m.rdblur  (params as attributes)
```
