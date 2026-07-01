---
name: notch
type: mul  # multiplicative
func: xsntch
n_params: 3
family: [notch]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelNotch.tex
---

# notch

**multiplicative model** (`mul`), function `xsntch`.

## Description

A notch line absorption. This is model is equivalent to a very saturated absorption line.

$$M(E) = \begin{array}{ll}
        (1-f) &  E_L - W/2 < E < E_L + W/2 \rowsp
        1 & \mbox{elsewhere}
       \end{array}$$

where

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 3.5 | 0 | 20 | 0 | 20 | 0.05 |  |
| 2 | Width | keV | 1 | 0 | 20 | 0 | 20 | 0.02 |  |
| 3 | CvrFract | — | 1 | 0 | 1 | 0 | 1 | 0.005 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("notch*powerlaw")
# component: m.notch  (params as attributes)
```
