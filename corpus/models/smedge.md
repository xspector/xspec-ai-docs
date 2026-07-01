---
name: smedge
type: mul  # multiplicative
func: xssmdg
n_params: 4
family: [smedge]
energy_range: [1.e-20, 1.e20]
source: manager/model.dat + XSmodelSmedge.tex
---

# smedge

**multiplicative model** (`mul`), function `xssmdg`.

## Description

A smeared edge (Ebisawa PhD thesis, implemented by Frank Marshall).

$$M(E) = \begin{array}{ll}
        1 & E < E_c\rowsp
        \exp\left[-f(E/E_c)^\alpha\right] \left[1-\exp((E_c-E)/W)\right]
           & E \geq E_c
       \end{array}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | edgeE | keV | 7 | 0.1 | 100 | 0.1 | 100 | 0.05 |  |
| 2 | MaxTau | — | 1 | 0 | 5 | 0 | 10 | 0.01 |  |
| 3 | index | — | -2.67 | -10 | 10 | -10 | 10 | 0.01 | frozen by default |
| 4 | width | — | 10 | 0.01 | 100 | 0.01 | 100 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("smedge*powerlaw")
# component: m.smedge  (params as attributes)
```
