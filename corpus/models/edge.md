---
name: edge
type: mul  # multiplicative
func: xsedge
n_params: 2
family: [edge, zedge]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelEdge.tex
---

# edge

**multiplicative model** (`mul`), function `xsedge`.

Variants documented together: `edge`, `zedge`.

## Description

The `edge` model is absorption edge, given by

$$M(E) = \begin{array}{ll}
         1 & E \leq E_c\rowsp
         exp\left[-D(E/E_c)^{-3}\right] & E \geq E_c
       \end{array}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | edgeE | keV | 7 | 0 | 100 | 0 | 100 | 0.05 |  |
| 2 | MaxTau | — | 1 | 0 | 5 | 0 | 10 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("edge*powerlaw")
# component: m.edge  (params as attributes)
```
