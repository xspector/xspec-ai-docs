---
name: vgaussian
type: add  # additive
func: C_vgaussianLine
n_params: 3
family: [vgauss, zvgauss]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVgauss.tex
---

# vgaussian

**additive model** (`add`), function `C_vgaussianLine`.

Variants documented together: `vgauss`, `zvgauss`.

## Description

A simple gaussian line profile with the sigma parameter as
velocity-width in km/s. If the width is $\leq 0$ then it is treated as a
delta function. The `zvgauss` variant computes a redshifted gaussian.

$$A(E) = K{1\over{(\sigma(E_l/c))*\sqrt{2*\pi}}} \exp\left({-(E-E_l)^2\over{2(\sigma(E_l/c))^2}}\right)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.5 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | km/s | 100 | 0 | 300000 | 0 | 300000 | 0.05 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vgaussian")
# component: m.vgaussian  (params as attributes)
```
