---
name: zvgabs
type: mul  # multiplicative
func: C_zvgaussianAbsorptionLine
n_params: 4
family: [vgabs, zvgabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVgabs.tex
---

# zvgabs

**multiplicative model** (`mul`), function `C_zvgaussianAbsorptionLine`.

Variants documented together: `vgabs`, `zvgabs`.

## Description

A gaussian absorption line as a multiplicative model with sigma in km/s. The zvgabs
variant includes redshift as a parameter.

$$M(E) = exp\left(-\left(par3/(\sqrt{2\pi}(par2/c))\right)
exp\left(-.5\left(\left(E-par1\right)/(par2/c)\right)^2\right)\right)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | km/s | 100 | 0 | 300000 | 0 | 300000 | 1 |  |
| 3 | Strength | keV | 1 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zvgabs*powerlaw")
# component: m.zvgabs  (params as attributes)
```
