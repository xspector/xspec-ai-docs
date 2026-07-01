---
name: redge
type: add  # additive
func: xredge
n_params: 3
family: [redge]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRedge.tex
---

# redge

**additive model** (`add`), function `xredge`.

## Description

Recombination edge emission.

$$A(E) = \left\{ \begin{array}{ll}
             0 & \mbox{if $E < E_c$} \\
             K(1/T_p)\exp[{-(E-E_c)\over{T_p}}] & \mbox{if $E >= E_c$} \\
              \end{array}
       \right.$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | edge | keV | 1.4 | 0.001 | 100 | 0.001 | 100 | 0.001 |  |
| 2 | kT | keV | 1 | 0.001 | 100 | 0.001 | 100 | 0.001 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("redge")
# component: m.redge  (params as attributes)
```
