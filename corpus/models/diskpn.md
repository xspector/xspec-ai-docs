---
name: diskpn
type: add  # additive
func: xsdiskpn
n_params: 3
family: [diskpn]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelDiskpn.tex
---

# diskpn

**additive model** (`add`), function `xsdiskpn`.

## Description

Blackbody spectrum of an accretion disk. This is an extension of the
`diskbb` model, including corrections for temperature distribution near
the black hole. The temperature distribution was calculated in
Paczynski-Wiita pseudo-Newtonian potential. An accretion rate can be
computed from the maximum temperature found.  For details see
[Gierlinski et al. (1999)](https://ui.adsabs.harvard.edu/abs/1999MNRAS.309..496G/abstract). Please note that the inner
disk radius (par2) can be a free parameter only close to par2 = 6;
otherwise par2 is strongly correlated with K.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | T_max | keV | 1 | 0.001 | 100 | 0.0001 | 200 | 0.01 |  |
| 2 | R_in | R_g | 6 | 6 | 1000 | 6 | 1000 | 0.1 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("diskpn")
# component: m.diskpn  (params as attributes)
```
