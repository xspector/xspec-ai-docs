---
name: zhighect
type: mul  # multiplicative
func: xszhcu
n_params: 3
family: [highecut, zhighect]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelHighecut.tex
---

# zhighect

**multiplicative model** (`mul`), function `xszhcu`.

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
| 1 | cutoffE | keV | 10 | 0.01 | 100 | 0.0001 | 200 | 0.01 |  |
| 2 | foldE | keV | 15 | 0.01 | 100 | 0.0001 | 200 | 0.01 |  |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zhighect*powerlaw")
# component: m.zhighect  (params as attributes)
```
