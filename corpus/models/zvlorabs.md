---
name: zvlorabs
type: mul  # multiplicative
func: C_zvlorentzianAbsorptionLine
n_params: 4
family: [vlorabs, zvlorabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVlorabs.tex
---

# zvlorabs

**multiplicative model** (`mul`), function `C_zvlorentzianAbsorptionLine`.

Variants documented together: `vlorabs`, `zvlorabs`.

## Description

A lorentzian absorption line with the line width in km/s as a
multiplicative model. The zlorabs variant includes redshift as a parameter.

$$M(E) = exp(-d*l(E))$$

$$l(E) = {\sigma(E_l/c)\over{(\pi-2\arctan(-2E_L/(\sigma(E_l/c))))}}{1\over{(E-E_L)^2 + (\sigma(E_l/c)/2)^2}}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | km/s | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Width | km/s | 100 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | Strength | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zvlorabs*powerlaw")
# component: m.zvlorabs  (params as attributes)
```
