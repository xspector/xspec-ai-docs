---
name: zvagauss
type: add  # additive
func: C_zvagauss
n_params: 4
family: [vagauss, zvagauss]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVagauss.tex
---

# zvagauss

**additive model** (`add`), function `C_zvagauss`.

Variants documented together: `vagauss`, `zvagauss`.

## Description

A simple gaussian line profile in wavelength. If the width is $\leq 0$ then it is treated
as a delta function. The zagauss variant computes a redshifted
gaussian.

$$A(\lambda) = K {1\over{(\sigma/c)\sqrt{2\pi}}}
\exp(-(\lambda-\lambda_l)^2/2(\sigma/c)^2)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | A | 10 | 0 | 1000000 | 0 | 1000000 | 0.01 |  |
| 2 | Sigma | km/s | 100 | 0 | 300000 | 0 | 300000 | 1 |  |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zvagauss")
# component: m.zvagauss  (params as attributes)
```
