---
name: bnei
type: add  # additive
func: C_bnei
n_params: 6
family: [nei, vnei, vvnei, bnei, bvnei, bvvnei]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelNei.tex
---

# bnei

**additive model** (`add`), function `C_bnei`.

Variants documented together: `nei`, `vnei`, `vvnei`, `bnei`, `bvnei`, `bvvnei`.

## Description

Non-equilibrium ionization collisional plasma model. This assumes a
constant temperature and single ionization parameter. It provides a
characterization of the spectrum but is not a physical model. The
references for this model can be found under the description of the
`equil` model. Several versions are available. To switch between them
use the `xset` **NEIAPECROOT** command. The versions available are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | Abundanc | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 3 | Tau | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bnei")
# component: m.bnei  (params as attributes)
```
