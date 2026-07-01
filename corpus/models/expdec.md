---
name: expdec
type: add  # additive
func: xsxpdec
n_params: 2
family: [expdec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelExpdec.tex
---

# expdec

**additive model** (`add`), function `xsxpdec`.

## Description

An exponential decay.

$$A(E) = K\exp(-\alpha E)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | factor | — | 1 | 0 | 100 | 0 | 100 | 0.01 |  |
| 2 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("expdec")
# component: m.expdec  (params as attributes)
```
