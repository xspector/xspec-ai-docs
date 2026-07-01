---
name: logpar
type: add  # additive
func: C_logpar
n_params: 4
family: [logpar, zlogpar]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLogpar.tex
---

# logpar

**additive model** (`add`), function `C_logpar`.

Variants documented together: `logpar`, `zlogpar`.

## Description

`logpar` is a power-law with an index which varies with energy
as a log parabola. The `zlogpar` variant computes a redshifted
spectrum. See for instance [Massaro et al. (2004)](https://ui.adsabs.harvard.edu/abs/2004A%26A...422..103M/abstract).

$$A(E) = K (E/pivotE)^{(-a-b\log{(E/pivotE)})}$$

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | alpha | — | 1.5 | 0 | 4 | 0 | 4 | 0.01 |  |
| 2 | beta | — | 0.2 | -4 | 4 | -4 | 4 | 0.01 |  |
| 3 | pivotE | keV | 1 |  |  |  |  |  | scale (not fitted) |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("logpar")
# component: m.logpar  (params as attributes)
```
