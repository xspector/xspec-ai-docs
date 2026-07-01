---
name: gnei
type: add  # additive
func: C_gnei
n_params: 6
family: [gnei, vgnei, vvgnei, bgnei, bvgnei, bvvgnei]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelGnei.tex
---

# gnei

**additive model** (`add`), function `C_gnei`.

Variants documented together: `gnei`, `vgnei`, `vvgnei`, `bgnei`, `bvgnei`, `bvvgnei`.

## Description

Non-equilibrium ionization collisional plasma model. This is a
generalization of the `nei` model where the temperature is allowed to
have been different in the past i.e. the ionization timescale averaged
temperature is not necessarily equal to the current temperature. For
example, in a standard Sedov model with equal electron and ion
temperatures, the ionization timescale averaged temperature is always
higher than the current temperature for each fluid element. The
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
| 4 | meankT | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("gnei")
# component: m.gnei  (params as attributes)
```
