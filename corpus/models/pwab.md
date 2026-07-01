---
name: pwab
type: mul  # multiplicative
func: xspwab
n_params: 3
family: [pwab]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelPwab.tex
---

# pwab

**multiplicative model** (`mul`), function `xspwab`.

## Description

An extension of partial covering fraction absorption into a power-law 
distribution of covering fraction as a function of column density, built 
from the `wabs` code.  See [Done & Magdziarz (1998)](https://ui.adsabs.harvard.edu/abs/1998MNRAS.298..737D/abstract) 
for details.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nHmin | 10^22 | 1 | 1e-07 | 100000 | 1e-07 | 1000000 | 0.001 |  |
| 2 | nHmax | 10^22 | 2 | 1e-07 | 100000 | 1e-07 | 1000000 | 0.001 |  |
| 3 | beta | — | 1 | -10 | 10 | -10 | 20 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("pwab*powerlaw")
# component: m.pwab  (params as attributes)
```
