---
name: equil
type: add  # additive
func: C_equil
n_params: 4
family: [equil, vequil, bequil, bvequil]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelEquil.tex
---

# equil

**additive model** (`add`), function `C_equil`.

Variants documented together: `equil`, `vequil`, `bequil`, `bvequil`.

## Description

Ionization equilibrium collisional plasma model. This is the
equilibrium version of Kazik Borkowski's NEI models. Several versions
are available. To switch between them use the `xset` **NEIAPECROOT**
command. The versions available are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | Abundanc | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("equil")
# component: m.equil  (params as attributes)
```
