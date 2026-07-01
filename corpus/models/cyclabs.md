---
name: cyclabs
type: mul  # multiplicative
func: xscycl
n_params: 5
family: [cyclabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCyclabs.tex
---

# cyclabs

**multiplicative model** (`mul`), function `xscycl`.

## Description

A cyclotron absorption line as used in pulsar spectra. See
[Mihara et al. (1990)](https://ui.adsabs.harvard.edu/abs/1990Natur.346..250M/abstract), or [Makishima et al. (1990)](https://ui.adsabs.harvard.edu/abs/1990ApJ...365L..59M/abstract). 

$$M(E)=exp\left[-D_f\frac{(W_fE/E_{cycl})^2}{(E-E_{cycl})^2+W_f^2} + 
D_{2h}\frac{(W_{2h}E/2E_{cycl})^2}{(E-2E_{cycl})^2+W_{2h}^2} \right]$$

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Depth0 | — | 2 | 0 | 100 | 0 | 100 | 0.01 |  |
| 2 | E0 | keV | 30 | 1 | 100 | 1 | 100 | 0.01 |  |
| 3 | Width0 | keV | 10 | 1 | 100 | 1 | 100 | 0.01 | frozen by default |
| 4 | Depth2 | — | 0 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 5 | Width2 | keV | 20 | 1 | 100 | 1 | 100 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("cyclabs*powerlaw")
# component: m.cyclabs  (params as attributes)
```
