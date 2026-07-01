---
name: zbknpower
type: add  # additive
func: C_zBrokenPowerLaw
n_params: 5
family: [bknpower, zbknpower]
energy_range: [-1.e20, 1.e20]
source: manager/model.dat + XSmodelBknpower.tex
---

# zbknpower

**additive model** (`add`), function `C_zBrokenPowerLaw`.

Variants documented together: `bknpower`, `zbknpower`.

## Description

`bknpower` is a broken power law and `zbknpower` a
redshifted variant.

$$A(E) =  \left\{ \begin{array}{ll}
          K E^{-\Gamma_1} & \mbox{if $E \leq E_{break}$} \\
          K E^{\Gamma_2-\Gamma_1}_{break} (E/1 keV)^{-\Gamma_2} &
          \mbox{if $E > E_{break}$} \\
                \end{array}
        \right.$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndx1 | — | 1 | -2 | 9 | -3 | 10 | 0.01 |  |
| 2 | BreakE | keV | 5 | 0.01 | 1000000 | 0 | 1000000 | 0.01 |  |
| 3 | PhoIndx2 | — | 2 | -2 | 9 | -3 | 10 | 0.01 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zbknpower")
# component: m.zbknpower  (params as attributes)
```
