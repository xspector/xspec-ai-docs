---
name: kyconv
type: con  # convolution
func: kyconv
n_params: 12
family: [kyconv]
energy_range: [0., 1.0e20]
source: manager/model.dat + XSmodelKyconv.tex
---

# kyconv

**convolution model** (`con`), function `kyconv`.

## Description

Convolution using as a kernel the relativistic line from an axisymmetic accretion disk. See
[Dovciak et al. (2004)](https://ui.adsabs.harvard.edu/abs/2004ApJS..153..205D/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | a | GM/c | 0.9982 | 0 | 1 | 0 | 1 | 0.2 |  |
| 2 | theta_o | deg | 30 | 0 | 89 | 0 | 89 | 5 |  |
| 3 | rin | GM/c^2 | 1 | 1 | 1000 | 1 | 1000 | 0.5 | frozen by default |
| 4 | ms | — | 1 | 0 | 1 | 0 | 1 | 1 | frozen by default |
| 5 | rout | GM/c^2 | 400 | 1 | 1000 | 1 | 1000 | 1 | frozen by default |
| 6 | alpha | — | 3 | -20 | 20 | -20 | 20 | 0.5 | frozen by default |
| 7 | beta | — | 3 | -20 | 20 | -20 | 20 | 0.5 | frozen by default |
| 8 | rb | GM/c^2 | 400 | 1 | 1000 | 1 | 1000 | 0.5 | frozen by default |
| 9 | zshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.1 | frozen by default |
| 10 | limb | — | 0 | 0 | 2 | 0 | 2 | 1 | frozen by default |
| 11 | ne_loc | — | 100 | 3 | 5000 | 3 | 5000 | 100 | frozen by default |
| 12 | normal | — | 1 | -1 | 100 | -1 | 100 | 1 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("kyconv*powerlaw")
# component: m.kyconv  (params as attributes)
```
