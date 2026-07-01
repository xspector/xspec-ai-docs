---
name: bpshock
type: add  # additive
func: C_bpshock
n_params: 7
family: [pshock, vpshock, vvpshock, bpshock, bvpshock, bvvpshock]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPshock.tex
---

# bpshock

**additive model** (`add`), function `C_bpshock`.

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
| 2 | Abundanc | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 3 | Tau_l | s/cm^3 | 0 | 0 | 50000000000000 | 0 | 50000000000000 | 100000000 | frozen by default |
| 4 | Tau_u | s/cm^3 | 100000000000 | 100000000 | 50000000000000 | 100000000 | 50000000000000 | 100000000 |  |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bpshock")
# component: m.bpshock  (params as attributes)
```
