---
name: vpshock
type: add  # additive
func: C_vpshock
n_params: 18
family: [pshock, vpshock, vvpshock, bpshock, bvpshock, bvvpshock]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPshock.tex
---

# vpshock

**additive model** (`add`), function `C_vpshock`.

Variants documented together: `pshock`, `vpshock`, `vvpshock`, `bpshock`, `bvpshock`, `bvvpshock`.

## Description

Constant temperature plane-parallel shock plasma model. The references
for this model can be found under the description of the
`equil` model. Several versions are available. To switch
between them use the `xset` **NEIAPECROOT** command. The versions
available are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | H | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 3 | He | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 4 | C | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 5 | N | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 6 | O | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 7 | Ne | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 8 | Mg | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 9 | Si | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 10 | S | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 11 | Ar | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 12 | Ca | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 13 | Fe | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 14 | Ni | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 15 | Tau_l | s/cm^3 | 0 | 0 | 50000000000000 | 0 | 50000000000000 | 100000000 | frozen by default |
| 16 | Tau_u | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 17 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 18 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vpshock")
# component: m.vpshock  (params as attributes)
```
