---
name: zpowerlw
type: add  # additive
func: C_zpowerLaw
n_params: 3
family: [powerlaw, zpowerlw]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPowerlaw.tex
---

# zpowerlw

**additive model** (`add`), function `C_zpowerLaw`.

Variants documented together: `powerlaw`, `zpowerlw`.

## Description

`powerlaw` is a simple photon power law. The
`zpowerlw` variant computes a redshifted spectrum.

$$A(E) = K E^{-\alpha}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 1 | -2 | 9 | -3 | 10 | 0.01 |  |
| 2 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zpowerlw")
# component: m.zpowerlw  (params as attributes)
```
