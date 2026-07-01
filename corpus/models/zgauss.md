---
name: zgauss
type: add  # additive
func: C_xszgau
n_params: 4
family: [gauss, zgauss]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelGauss.tex
---

# zgauss

**additive model** (`add`), function `C_xszgau`.

Variants documented together: `gauss`, `zgauss`.

## Description

A simple gaussian line profile. If the width is $\leq 0$ then it is treated as a
delta function. The `zgauss` variant computes a redshifted gaussian.

$$A(E) = K{2\over{\sigma\sqrt{2\pi}(1-\mathit{erf}(-E_l/(\sqrt{2}\sigma)))}} \exp\left({-(E-E_l)^2\over{2\sigma^2}}\right)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.5 | 0 | 1000000 | 0 | 1000000 | 0.05 |  |
| 2 | Sigma | keV | 0.1 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zgauss")
# component: m.zgauss  (params as attributes)
```
