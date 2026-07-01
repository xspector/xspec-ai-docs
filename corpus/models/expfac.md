---
name: expfac
type: mul  # multiplicative
func: xsexp
n_params: 3
family: [expfac]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelExpfac.tex
---

# expfac

**multiplicative model** (`mul`), function `xsexp`.

## Description

An exponential modification of a spectrum.

$$M(E) = \begin{array}{ll}
        1+Aexp(-fE) & E > E_c\rowsp
        1 & E < E_c
       \end{array}$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Ampl | — | 1 | 0 | 100000 | 0 | 1000000 | 0.01 |  |
| 2 | Factor | — | 1 | 0 | 100000 | 0 | 1000000 | 0.01 |  |
| 3 | StartE | keV | 0.5 | 0 | 100000 | 0 | 1000000 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("expfac*powerlaw")
# component: m.expfac  (params as attributes)
```
