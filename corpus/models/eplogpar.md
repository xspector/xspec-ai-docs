---
name: eplogpar
type: add  # additive
func: eplogpar
n_params: 3
family: [eplogpar]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelEplogpar.tex
---

# eplogpar

**additive model** (`add`), function `eplogpar`.

## Description

$ normalization}eplogpar is a power-law with an index which varies with energy as a log parabola.

$$A(E) = 10^{-\beta(\log(E/E_p))^2} / E^2$$

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Ep | keV | 0.1 | 1e-06 | 100 | 1e-10 | 10000 | 0.01 |  |
| 2 | beta | — | 0.2 | -4 | 4 | -4 | 4 | 0.01 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("eplogpar")
# component: m.eplogpar  (params as attributes)
```
