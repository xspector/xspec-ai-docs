---
name: xscat
type: mul  # multiplicative
func: C_xscatmodel
n_params: 4
family: [xscat]
energy_range: [0.0, 1.e20]
source: manager/model.dat + XSmodelXscat.tex
---

# xscat

**multiplicative model** (`mul`), function `C_xscatmodel`.

## Description

This model calculates the X-ray scattering cross section of
a population of dust grains as a function of energy, given a specific
dust grain position and an extraction region.  As the grain position
gets closer to the source of the X-rays for a constant extraction
region, the cross section drops as more X-rays remain within the
extraction circle.  For constant dust grain position, the cross
section decreases with increasing extraction region size because more 
photons remain within it. 

A detailed description of the model can be found in [Smith, Valencic &
Corrales (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...818..143S/abstract).

The model parameters are as follows.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | NH | 10^22 | 1 | 0 | 1000 | 0 | 1000 | 0.1 |  |
| 2 | Xpos | — | 0.5 | 0 | 0.99 | 0 | 0.999 | 0.01 |  |
| 3 | Rext | arcsec | 10 | 0 | 235 | 0 | 240 | 1 | frozen by default |
| 4 | DustModel | — | 1 |  |  |  |  |  | switch (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("xscat*powerlaw")
# component: m.xscat  (params as attributes)
```
