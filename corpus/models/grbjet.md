---
name: grbjet
type: add  # additive
func: c_xsgrbjet
n_params: 14
family: [grbjet]
energy_range: [1.e-20, 1.e+20]
source: manager/model.dat + XSmodelGrbjet.tex
---

# grbjet

**additive model** (`add`), function `c_xsgrbjet`.

## Description

This model computes the time-averaged flux over the signal duration
determined by the radiation curvature effect for a single pulse
emitted by a relativistic top-hat jet ([Farinelli et al., 2021](https://ui.adsabs.harvard.edu/abs/2021MNRAS.501.5723F/abstract)).

The parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | thobs | — | 5 | 0 | 30 | 0 | 30 | 0.01 | frozen by default |
| 2 | thjet | — | 10 | 2 | 20 | 2 | 20 | 0.01 | frozen by default |
| 3 | gamma | — | 200 | 1 | 500 | 1 | 500 | 0.01 |  |
| 4 | r12 | — | 1 | 0.1 | 100 | 0.1 | 100 | 0.01 | frozen by default |
| 5 | p1 | — | 0 | -2 | 1 | -2 | 1 | 0.01 |  |
| 6 | p2 | — | 1.5 | 1.1 | 10 | 1.1 | 10 | 0.01 |  |
| 7 | E0 | keV | 1 | 0.1 | 1000 | 0.1 | 1000 | 0.01 |  |
| 8 | delta | — | 0.2 | 0.01 | 1.5 | 0.01 | 1.5 | 0.01 | frozen by default |
| 9 | index_pl | — | 0.8 | 0 | 1.5 | 0 | 1.5 | 0.01 | frozen by default |
| 10 | ecut | keV | 20 | 0.1 | 1000 | 0.1 | 1000 | 0.01 | frozen by default |
| 11 | ktbb | keV | 1 | 0.1 | 1000 | 0.1 | 1000 | 0.01 | frozen by default |
| 12 | model | — | 1 |  |  |  |  |  | switch (not fitted) |
| 13 | redshift | — | 2 | 0.01 | 10 | 0.001 | 10 | 1 | frozen by default |
| 14 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("grbjet")
# component: m.grbjet  (params as attributes)
```
