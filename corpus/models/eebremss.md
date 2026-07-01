---
name: eebremss
type: add  # additive
func: C_eebremss
n_params: 4
family: [eebremss]
energy_range: [0.0, 1.e20]
source: manager/model.dat + XSmodelEebremss.tex
---

# eebremss

**additive model** (`add`), function `C_eebremss`.

## Description

The emission due to electron-electron bremsstrahlug from a
collisionally-ionized gas. Uses the approximations from
[Nozawa et al
  (2009)](https://ui.adsabs.harvard.edu/abs/2009A%26A...499..661N/abstract). This component is
already included in all the apec-derived models if APECEEBREMSS is xset to yes.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | T | keV | 1 | 0.05 | 10000000000 | 0.05 | 10000000000 | 0.01 |  |
| 2 | eperh | — | 1.2 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("eebremss")
# component: m.eebremss  (params as attributes)
```
