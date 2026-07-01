---
name: plabs
type: mul  # multiplicative
func: xsplab
n_params: 2
family: [plabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPlabs.tex
---

# plabs

**multiplicative model** (`mul`), function `xsplab`.

## Description

Absorption as a power-law in energy. Useful for things like dust.

$$M(E) = KE^{-\alpha}$$

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | index | — | 2 | 0 | 5 | 0 | 5 | 0.01 |  |
| 2 | coef | — | 1 | 0 | 100 | 0 | 100 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("plabs*powerlaw")
# component: m.plabs  (params as attributes)
```
