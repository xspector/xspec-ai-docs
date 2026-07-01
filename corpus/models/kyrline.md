---
name: kyrline
type: add  # additive
func: kyrline
n_params: 12
family: [kyrline]
energy_range: [0., 1.0e20]
source: manager/model.dat + XSmodelKyrline.tex
---

# kyrline

**additive model** (`add`), function `kyrline`.

## Description

Relativistic line emission from an axisymmetic accretion disk. See
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
| 6 | Erest | keV | 6.4 | 1 | 99 | 1 | 99 | 0.01 | frozen by default |
| 7 | alpha | — | 3 | -20 | 20 | -20 | 20 | 0.5 | frozen by default |
| 8 | beta | — | 3 | -20 | 20 | -20 | 20 | 0.5 | frozen by default |
| 9 | rb | GM/c^2 | 400 | 1 | 1000 | 1 | 1000 | 0.5 | frozen by default |
| 10 | zshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.1 | frozen by default |
| 11 | limb | — | 1 | 0 | 2 | 0 | 2 | 1 | frozen by default |
| 12 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("kyrline")
# component: m.kyrline  (params as attributes)
```
