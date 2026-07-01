---
name: zcutoffpl
type: add  # additive
func: C_zcutoffPowerLaw
n_params: 4
family: [cutoffpl, zcutoffpl]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelCutoffpl.tex
---

# zcutoffpl

**additive model** (`add`), function `C_zcutoffPowerLaw`.

Variants documented together: `cutoffpl`, `zcutoffpl`.

## Description

A power law with high energy exponential rolloff.

$$A(E) = K E^{-\alpha} \exp(-E/\beta)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 1 | -2 | 9 | -3 | 10 | 0.01 |  |
| 2 | HighECut | keV | 15 | 1 | 500 | 0.01 | 500 | 0.01 |  |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zcutoffpl")
# component: m.zcutoffpl  (params as attributes)
```
