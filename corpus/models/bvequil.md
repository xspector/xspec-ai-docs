---
name: bvequil
type: add  # additive
func: C_bvequil
n_params: 16
family: [equil, vequil, bequil, bvequil]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelEquil.tex
---

# bvequil

**additive model** (`add`), function `C_bvequil`.

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
| 2 | He | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 3 | C | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 4 | N | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 5 | O | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 6 | Ne | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 7 | Mg | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 8 | Si | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 9 | S | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 10 | Ar | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 11 | Ca | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 12 | Fe | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 13 | Ni | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 14 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 15 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 16 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bvequil")
# component: m.bvequil  (params as attributes)
```
