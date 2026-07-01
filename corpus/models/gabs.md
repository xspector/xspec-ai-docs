---
name: gabs
type: mul  # multiplicative
func: C_gaussianAbsorptionLine
n_params: 3
family: [gabs, zgabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelGabs.tex
---

# gabs

**multiplicative model** (`mul`), function `C_gaussianAbsorptionLine`.

Variants documented together: `gabs`, `zgabs`.

## Description

A gaussian absorption line as a multiplicative model. The zgabs
variant includes redshift as a parameter.

$$M(E) = exp(-d*g(E))$$

$$g(E) = {2\over{\sigma\sqrt{2\pi}(1-\mathit{erf}(-E_l/(\sigma\sqrt{2})))}}
  \exp\left({-(E-E_l)^2\over{2\sigma^2}}\right)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | keV | 0.01 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | Strength | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |

## PyXspec

```python
from xspec import Model
m = Model("gabs*powerlaw")
# component: m.gabs  (params as attributes)
```
