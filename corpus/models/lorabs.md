---
name: lorabs
type: mul  # multiplicative
func: C_lorentzianAbsorptionLine
n_params: 3
family: [lorabs, zlorabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLorabs.tex
---

# lorabs

**multiplicative model** (`mul`), function `C_lorentzianAbsorptionLine`.

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

## PyXspec

```python
from xspec import Model
m = Model("lorabs*powerlaw")
# component: m.lorabs  (params as attributes)
```
