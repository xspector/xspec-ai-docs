---
name: zlorabs
type: mul  # multiplicative
func: C_zlorentzianAbsorptionLine
n_params: 4
family: [lorabs, zlorabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLorabs.tex
---

# zlorabs

**multiplicative model** (`mul`), function `C_zlorentzianAbsorptionLine`.

Variants documented together: `lorabs`, `zlorabs`.

## Description

A lorentzian absorption line as a multiplicative model. The zlorabs
variant includes redshift as a parameter.

$$M(E) = exp(-d*l(E))$$

$$l(E) = {\sigma\over{(\pi-2\arctan(-2E_L/\sigma))}}{1\over{(E-E_L)^2 + (\sigma/2)^2}}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Width | keV | 0.01 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | Strength | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zlorabs*powerlaw")
# component: m.zlorabs  (params as attributes)
```
