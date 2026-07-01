---
name: bkn2pow
type: add  # additive
func: C_broken2PowerLaw
n_params: 6
family: [bkn2pow]
energy_range: [-1.e20, 1.e20]
source: manager/model.dat + XSmodelBkn2pow.tex
---

# bkn2pow

**additive model** (`add`), function `C_broken2PowerLaw`.

## Description

A three-segment broken power law (i.e. with two break energies).

$$A(E) =  \left\{ \begin{array}{ll}
          K E^{-\Gamma_1} & \mbox{if $E \leq E_{break,1}$} \\
          K E^{\Gamma_2-\Gamma_1}_{break,1} (E/1 keV)^{-\Gamma_2} &
          \mbox{if $E_{break,1} \leq E \leq E_{break,2}$} \\
          K E^{\Gamma_2-\Gamma_1}_{break,1} E^{\Gamma_3-\Gamma_2}_{break,2} (E/1 keV)^{-\Gamma_3} &
          \mbox{if $E_{break,2} \leq E$} \\
                \end{array}
        \right.$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndx1 | — | 1 | -2 | 9 | -3 | 10 | 0.01 |  |
| 2 | BreakE1 | keV | 5 | 0.01 | 1000000 | 0 | 1000000 | 0.01 |  |
| 3 | PhoIndx2 | — | 2 | -2 | 9 | -3 | 10 | 0.01 |  |
| 4 | BreakE2 | keV | 10 | 0.01 | 1000000 | 0 | 1000000 | 0.01 |  |
| 5 | PhoIndx3 | — | 3 | -2 | 9 | -3 | 10 | 0.01 |  |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bkn2pow")
# component: m.bkn2pow  (params as attributes)
```
