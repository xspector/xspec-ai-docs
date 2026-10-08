---
name: gsmooth
type: con  # convolution
func: C_gsmooth
n_params: 2
family: [gsmooth]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelGsmooth.tex
---

# gsmooth

**convolution model** (`con`), function `C_gsmooth`.

## Description

Gaussian smoothing with a variable width $\Sigma(E)$, which varies as the 
par2 power of the energy. The width at 6 keV is set with par1.

$$dC(E) = \frac{1}{\sqrt{2\pi\Sigma(E)^2}}\exp\left[-\frac{1}{2}\left(\frac{E-X}{\Sigma(E)}\right)^2\right]A(X)dX$$

$$\Sigma(E) = \sigma(E/6)^\alpha$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Sig_6keV | keV | 1 | 0 | 10 | 0 | 20 | 0.05 |  |
| 2 | Index | — | 0 | -1 | 1 | -1 | 1 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("gsmooth*powerlaw")
# component: m.gsmooth  (params as attributes)
```
