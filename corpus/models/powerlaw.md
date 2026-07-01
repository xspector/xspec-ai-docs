---
name: powerlaw
type: add  # additive
func: C_powerLaw
n_params: 2
family: [powerlaw, zpowerlw]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPowerlaw.tex
---

# powerlaw

**additive model** (`add`), function `C_powerLaw`.

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
| 2 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("powerlaw")
# component: m.powerlaw  (params as attributes)
```
