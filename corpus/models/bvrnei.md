---
name: bvrnei
type: add  # additive
func: C_bvrnei
n_params: 19
family: [rnei, vrnei, vvrnei, brnei, bvrnei, bvvrnei]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRnei.tex
---

# bvrnei

**additive model** (`add`), function `C_bvrnei`.

Variants documented together: `rnei`, `vrnei`, `vvrnei`, `brnei`, `bvrnei`, `bvvrnei`.

## Description

Non-equilibrium ionization collisional plasma model. This is a model
for a recombining plasma where the plasma is
assumed to have started in collisional equilibrium with the initial
temperature given by the relevant input parameter. This model will
only work for `xset` **NEIAPECROOT 3.0** and above. Additional 
`xset` options are available and are listed under the
documentation for `nei`.

For the `rnei` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 0.5 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | kT_init | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 3 | H | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 4 | He | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 5 | C | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 6 | N | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 7 | O | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 8 | Ne | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 9 | Mg | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 10 | Si | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 11 | S | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 12 | Ar | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 13 | Ca | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 14 | Fe | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 15 | Ni | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 16 | Tau | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 17 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 18 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 19 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bvrnei")
# component: m.bvrnei  (params as attributes)
```
