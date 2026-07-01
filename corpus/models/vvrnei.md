---
name: vvrnei
type: add  # additive
func: C_vvrnei
n_params: 35
family: [rnei, vrnei, vvrnei, brnei, bvrnei, bvvrnei]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRnei.tex
---

# vvrnei

**additive model** (`add`), function `C_vvrnei`.

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
| 3 | H | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | Li | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | Be | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | B | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | F | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | P | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 18 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 19 | Cl | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 20 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 21 | K | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 22 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 23 | Sc | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 24 | Ti | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 25 | V | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 26 | Cr | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 27 | Mn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 28 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 29 | Co | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 30 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 31 | Cu | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 32 | Zn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 33 | Tau | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 34 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 35 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vvrnei")
# component: m.vvrnei  (params as attributes)
```
