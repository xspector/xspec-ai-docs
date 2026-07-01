---
name: rnei
type: add  # additive
func: C_rnei
n_params: 6
family: [rnei, vrnei, vvrnei, brnei, bvrnei, bvvrnei]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRnei.tex
---

# rnei

**additive model** (`add`), function `C_rnei`.

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
| 3 | Abundanc | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 4 | Tau | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("rnei")
# component: m.rnei  (params as attributes)
```
