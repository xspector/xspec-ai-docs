---
name: agauss
type: add  # additive
func: C_agauss
n_params: 3
family: [agauss, zagauss]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelAgauss.tex
---

# agauss

**additive model** (`add`), function `C_agauss`.

Variants documented together: `agauss`, `zagauss`.

## Description

A simple gaussian line profile. If the width is $\leq 0$ then it is treated
as a delta function. The zagauss variant computes a redshifted
gaussian.

$$A(\lambda) = K {1\over{\sigma\sqrt{2\pi}}}
\exp(-(\lambda-\lambda_l)^2/2\sigma^2)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | A | 10 | 0 | 1000000 | 0 | 1000000 | 0.01 |  |
| 2 | Sigma | A | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("agauss")
# component: m.agauss  (params as attributes)
```
