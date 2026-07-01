---
name: highecut
type: mul  # multiplicative
func: xshecu
n_params: 2
family: [highecut, zhighect]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelHighecut.tex
---

# highecut

**multiplicative model** (`mul`), function `xshecu`.

Variants documented together: `highecut`, `zhighect`.

## Description

A high energy cutoff.

$$M(E) = \begin{array}{ll}
        exp\left[(E_c-E)/E_f\right] & E \geq E_c\rowsp
        1.0 & E \leq E_c
       \end{array}$$

where

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | cutoffE | keV | 10 | 0.01 | 1000000 | 0.0001 | 1000000 | 0.01 |  |
| 2 | foldE | keV | 15 | 0.01 | 1000000 | 0.0001 | 1000000 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("highecut*powerlaw")
# component: m.highecut  (params as attributes)
```
